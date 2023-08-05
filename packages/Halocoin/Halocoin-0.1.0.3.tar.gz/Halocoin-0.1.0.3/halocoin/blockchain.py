import copy
import queue
import time
from cdecimal import Decimal

from halocoin import custom, api
from halocoin import tools
from halocoin.ntwrk import Response
from halocoin.service import Service, threaded, sync, NoExceptionQueue


class BlockchainService(Service):
    tx_types = ['spend', 'mint']
    IDLE = 1
    SYNCING = 2

    def __init__(self, engine):
        Service.__init__(self, name='blockchain')
        self.engine = engine
        self.blocks_queue = NoExceptionQueue(3)
        self.tx_queue = NoExceptionQueue(100)
        self.db = None
        self.account = None
        self.in_memory_db = {}
        self.__state = BlockchainService.IDLE

    def on_register(self):
        self.db = self.engine.db
        self.account = self.engine.account
        print("Started Blockchain")
        return True

    @threaded
    def process_blocks(self):
        try:
            candidate_block = self.blocks_queue.get(timeout=1)
        except queue.Empty:
            return
        self.set_chain_state(BlockchainService.SYNCING)
        try:
            if isinstance(candidate_block, list):
                blocks = candidate_block  # This is just aliasing

                integrity_flag = True
                for block in blocks:
                    if not BlockchainService.block_integrity_check(block):
                        integrity_flag = False
                        break

                if integrity_flag:
                    length = self.db.get('length')
                    for i in range(20):
                        block = self.db.get(length)
                        if BlockchainService.fork_check(blocks, length, block):
                            self.delete_block()
                            length -= 1
                        else:
                            break
                    for block in blocks:
                        self.add_block(block)
            else:
                self.add_block(candidate_block)
            self.set_chain_state(BlockchainService.IDLE)
        except:
            self.set_chain_state(BlockchainService.IDLE)
        self.blocks_queue.task_done()

    @threaded
    def process_txs(self):
        try:
            candidate_tx = self.tx_queue.get(timeout=1)
        except queue.Empty:
            return
        self.add_tx(candidate_tx)
        self.tx_queue.task_done()

    @sync
    def set_chain_state(self, new_state):
        self.__state = new_state

    @sync
    def get_chain_state(self):
        return self.__state

    @sync
    def tx_pool(self):
        """
        Return all the transactions waiting in the pool.
        This method should be used instead of direct access to db
        :return:
        """
        return self.db.get('txs')

    @sync
    def tx_pool_add(self, tx):
        """
        This is an atomic add operation for txs pool.
        :param tx: Transaction to be added
        :return: None
        """
        txs = self.db.get('txs')
        txs.append(tx)
        api.new_tx_in_pool()
        self.db.put('txs', txs)

    @sync
    def tx_pool_pop_all(self):
        """
        Atomic operation to pop everything
        :return: transactions list
        """
        txs = self.db.get('txs')
        self.db.put('txs', [])
        return txs

    def add_tx(self, tx):

        if not isinstance(tx, dict):
            return False

        address = tools.tx_owner_address(tx)

        # tools.log('attempt to add tx: ' +str(tx))
        txs_in_pool = self.tx_pool()

        response = Response(True, None)
        if 'type' not in tx or not isinstance(tx['type'], str) \
                or tx['type'] not in BlockchainService.tx_types:
            response.setData('type error')
            response.setFlag(False)
        if tx in txs_in_pool:
            response.setData('no duplicates')
            response.setFlag(False)
        if not BlockchainService.tx_integrity_check(tx).getFlag():
            response.setData('tx: ' + str(tx))
            response.setFlag(False)
        if tx['count'] != self.account.known_tx_count(tools.tx_owner_address(tx)):
            response.setData('count error')
            response.setFlag(False)
        if not self.account.is_tx_affordable(address, tx):
            response.setData('fee check error')
            response.setFlag(False)

        if response.getFlag():
            self.tx_pool_add(tx)
            return 'added tx into the pool: ' + str(tx)
        else:
            return 'failed to add tx because: ' + response.getData()

    def add_block(self, block):
        """Attempts adding a new block to the blockchain.
         Median is good for weeding out liars, so long as the liars don't have 51%
         hashpower. """

        length = self.db.get('length')

        if int(block['length']) != int(length) + 1:
            # tools.log('Length is not valid')
            return False

        if (length >= 0 and block['diffLength'] != tools.hex_sum(self.db.get('diffLength'), tools.hex_invert(block['target']))) \
                or (length < 0 and block['diffLength'] != tools.hex_invert(block['target'])):
            tools.log(block['diffLength'])
            tools.log(tools.hex_sum(self.db.get('diffLength'), tools.hex_invert(block['target'])))
            tools.log(block['length'])
            tools.log('difflength is wrong')
            return False

        if length >= 0 and tools.det_hash(self.db.get(length)) != block['prevHash']:
            tools.log('prevhash different')
            return False

        nonce_and_hash = tools.hash_without_nonce(block)
        if tools.det_hash(nonce_and_hash) > block['target']:
            tools.log('hash value does not match the target')
            return False

        if block['target'] != self.target(block['length']):
            tools.log('block: ' + str(block))
            tools.log('target: ' + str(self.target(block['length'])))
            tools.log('wrong target')
            return False

        recent_time_values = self.recent_blockthings('times', custom.mmm, self.db.get('length'))
        median_block = tools.median(recent_time_values)
        if block['time'] < median_block:
            tools.log('Received block is generated earlier than median.')
            return False

        if not self.account.update_accounts_with_block(block, add_flag=True, simulate=True):
            tools.log('Received block failed transactions check.')
            return False

        self.db.put(block['length'], block)
        self.db.put('length', block['length'])
        self.db.put('diffLength', block['diffLength'])

        orphans = self.tx_pool_pop_all()

        self.account.update_accounts_with_block(block, add_flag=True)

        for orphan in sorted(orphans, key=lambda x: x['count']):
            self.add_tx(orphan)

        from halocoin import api
        api.new_block()
        return True

    def delete_block(self):
        """ Removes the most recent block from the blockchain. """
        length = self.db.get('length')
        if length < 0:
            return

        targets = self.db.get('targets')
        if str(length) in targets:
            targets.pop(str(length))
        self.db.put('targets', targets)

        times = self.db.get('times')
        if str(length) in times:
            times.pop(str(length))
        self.db.put('times', times)

        block = self.db.get(length)
        self.account.update_accounts_with_block(block, add_flag=False)

        orphans = self.tx_pool_pop_all()

        for tx in block['txs']:
            orphans.append(tx)

        self.db.delete(length)
        length -= 1

        self.db.put('length', length)
        if length == -1:
            self.db.put('diffLength', '0')
        else:
            block = self.db.get(length)
            self.db.put('diffLength', block['diffLength'])

        for orphan in sorted(orphans, key=lambda x: x['count']):
            self.add_tx(orphan)

        return True

    @staticmethod
    def block_integrity_check(block):
        if not isinstance(block, dict):
            tools.log('Block is not a dict')
            return False

        if 'error' in block:
            tools.log('Errors in block')
            return False

        if not ('length' in block and isinstance(block['length'], int)):
            return False

        if 'version' not in block or block['version'] != custom.version:
            return False

        if 'target' not in block:
            tools.log('no target in block')
            return False

        if 'time' not in block:
            tools.log('no time')
            return False

        if block['time'] > time.time() + 60 * 6:
            tools.log('Received block is coming from future. Call the feds')
            return False

        return True

    def recent_blockthings(self, key, size, length=0):
        if length == 0:
            length = self.db.get('length')

        if key in self.in_memory_db:
            storage = self.in_memory_db[key]
        else:
            storage = self.db.get(key)
        start = max((length - size), 0)
        result = []
        for i in range(start, length):
            leng = str(i)
            if not leng in storage:
                storage[leng] = self.db.get(leng)[key[:-1]]  # Remove last character that is 's' e.g. targets => target
            result.append(storage[leng])
        self.in_memory_db[key] = storage
        self.db.put(key, storage)
        return result

    @staticmethod
    def sigs_match(_sigs, _pubs, msg):
        pubs = copy.deepcopy(_pubs)
        sigs = copy.deepcopy(_sigs)

        def match(sig, pubs, msg):
            for p in pubs:
                if tools.signature_verify(msg, sig, p):
                    return {'bool': True, 'pub': p}
            return {'bool': False}

        for sig in sigs:
            a = match(sig, pubs, msg)
            if not a['bool']:
                return False
            sigs.remove(sig)
            pubs.remove(a['pub'])
        return True

    @staticmethod
    def tx_signature_check(tx):
        tx_copy = copy.deepcopy(tx)
        if 'signatures' not in tx or not isinstance(tx['signatures'], (list,)):
            tools.log('no signatures')
            return False
        if 'pubkeys' not in tx or not isinstance(tx['pubkeys'], (list,)):
            tools.log('no pubkeys')
            return False
        if len(tx['pubkeys']) == 0:
            tools.log('pubkey error')
            return False
        if len(tx['signatures']) > len(tx['pubkeys']):
            tools.log('there are more signatures than required')
            return False

        tx_copy.pop('signatures')
        msg = tools.det_hash(tx_copy)
        if not BlockchainService.sigs_match(copy.deepcopy(tx['signatures']),
                                            copy.deepcopy(tx['pubkeys']), msg):
            tools.log('sigs do not match')
            return False
        return True

    @staticmethod
    def fork_check(newblocks, length, top_block_on_chain):
        """
        Check whether a fork happens while adding these blocks.
        If a fork is detected, return the index of last matched block.
        :param newblocks: Received blocks.
        :param length:
        :param top_block_on_chain:
        :return:
        """
        recent_hash = tools.det_hash(top_block_on_chain)
        their_hashes = list(map(lambda x: x['prevHash'] if x['length'] > 0 else 0, newblocks))
        their_hashes += [tools.det_hash(newblocks[-1])]
        b = (recent_hash not in their_hashes) and newblocks[0]['length'] - 1 < length < newblocks[-1]['length']
        return b

    @staticmethod
    def tx_integrity_check(tx):
        """
        This functions test whether a transaction has basic things right.
        Does it have amount, recipient, right signatures and correct address types.
        :param tx:
        :param txs: These txs can come from both pool and block.
        :return:
        """
        response = Response(True, None)
        if tx['type'] == 'spend':
            if 'to' not in tx or not isinstance(tx['to'], str):
                response.setData('no to')
                response.setFlag(False)
            if not BlockchainService.tx_signature_check(tx):
                response.setData('signature check')
                response.setFlag(False)
            if len(tx['to']) <= 30:
                response.setData('that address is too short ' + 'tx: ' + str(tx))
                response.setFlag(False)
            if 'amount' not in tx or not isinstance(tx['amount'], (int)):
                response.setData('no amount')
                response.setFlag(False)
        else:
            response.setFlag(False)
            response.setData('only spend transactions can be cheched')
        return response

    def target(self, length):
        """ Returns the target difficulty at a particular blocklength. """
        if length < 4:
            return bytearray.fromhex('0' * 4 + 'f' * 60)  # Use same difficulty for first few blocks.

        def targetTimesFloat(target, number):
            a = int(str(target), 16)
            b = int(a * number)  # this should be rational multiplication followed by integer estimation
            return tools.buffer_(format(b, 'x'), 64)

        def weights(length):  # uses float
            # returns from small to big
            out = custom.memoized_weights[:length]
            out.reverse()
            return out

        def estimate_target():
            """
            We are actually interested in the average number of hashes required to
            mine a block. number of hashes required is inversely proportional
            to target. So we average over inverse-targets, and inverse the final
            answer. """

            def sumTargets(l):
                if len(l) < 1:
                    return 0
                while len(l) > 1:
                    l = [tools.hex_sum(l[0], l[1])] + l[2:]
                return l[0]

            targets = self.recent_blockthings('targets', custom.history_length)
            w = weights(len(targets))  # should be rat instead of float
            tw = sum(w)
            targets = list(map(tools.hex_invert, targets))

            weighted_targets = [targetTimesFloat(targets[i], w[i] / tw) for i in range(len(targets))]
            return tools.hex_invert(sumTargets(weighted_targets))

        def estimate_time():
            times = self.recent_blockthings('times', custom.history_length)
            times = list(map(Decimal, times))
            # How long it took to generate blocks
            block_times = [times[i] - times[i - 1] for i in range(1, len(times))]
            w = weights(len(block_times))  # Geometric weighting
            tw = sum(w)
            return sum([w[i] * block_times[i] / tw for i in range(len(block_times))])

        retarget = estimate_time() / custom.blocktime
        result = targetTimesFloat(estimate_target(), retarget)
        return bytearray.fromhex(result)

