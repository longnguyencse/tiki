import traceback
import functools
import logging
import os
import traceback

def create_logger():
    """
    Creates a logging object and returns it
    """
    logger = logging.getLogger("example_logger")
    logger.setLevel(logging.INFO)
    # create the logging file handler
    dir_path = os.path.dirname(os.path.realpath(__file__))
    fh = logging.FileHandler('{}/log_err_app.log'.format(dir_path))
    fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)
    # add handler to logger object
    logger.addHandler(fh)
    return logger


def exception_logging(function):
    """
    A decorator that wraps the passed in function and logs
    exceptions should one occur
    """

    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        logger = create_logger()
        try:
            return function(*args, **kwargs)
        except Exception as e:
            tb = traceback.format_exc()
            # log the exception
            err = "There was an exception in  "
            err += function.__name__
            logger.exception(err)
            print('{}___/n__{}'.format(err, tb))
            # re-raise the exception
            raise
    return wrapper


class ADDRESS:
    HANOI_ADDR = 'HaNoi'
    HCM_ADDR = 'HCM'
    DANANG_ADDR = 'DaNang'
    HUE_ADDR = 'Hue'

class Item:
    BOOK = 'book'
    PEN = 'pen'


class Sol:
    ADDRESS = 'address'
    ITEMS = 'items'
    WH_NAME = 'wh_name'

    def __init__(self):
        self._ware_house = []

    @exception_logging
    def add_ware_house(self, ware_house):
        """
        ware_house = {address: ADDRESS.HANOI_ADDR, item: { Item.books: 2, Item.pens: 3}}
        :param ware_house:
        :return:
        """
        self._ware_house.append(ware_house)

    @exception_logging
    def make_choose_ware_house(self, order):
        """
        order = { address: ADDRESS.HANOI_ADDR, items: { Item.books: 2, Item.pens: 3}}
        :param order:
        :return:
        """
        candidates = []
        order_original = order.copy()
        rs = []
        for ware_house in self._ware_house:
            for name, quality in order_original[self.ITEMS].items():
                if ware_house.get(self.ITEMS, {}).get(name, 0) > 0:
                    candidates.append(ware_house)
                    break
        return self.__check_condition(candidates, order, rs)

    @exception_logging
    def __check_condition(self, candidates, order, rs):
        """
        check condition
        :param candidates:
        :param order:
        :return:
        """
        try:
            ware_house = self.__check_first_condition(candidates, order)
            if not ware_house:
                print(' STRAGE: check warehouse none --> need to check')
                return
            for name, quality in order.get(self.ITEMS, {}).items():
                if name in ware_house.get(self.ITEMS, {}).keys():
                    stock = float(ware_house.get(self.ITEMS).get(name))
                    amount = float(order.get(self.ITEMS).get(name))
                    max_supply = stock if amount > stock else amount
                    # update stock
                    ware_house.get(self.ITEMS).update({
                        name: stock - max_supply
                    })
                    # update remain purchase
                    order[self.ITEMS].update({
                        name: amount - max_supply
                    })
                    # update result
                    rs.append({self.WH_NAME: ware_house[self.WH_NAME], self.ITEMS: {name: max_supply}})
            for name, quality in order.get(self.ITEMS, {}).items():
                if quality > 0:
                    self.__check_condition(candidates, order, rs)
            # end
            print(f'END sol, result is {rs}')
            return rs
        except Exception:
            tb = traceback.format_exc()
            print(f'ERROR {tb}')

    @exception_logging
    def __check_first_condition(self, candidates, order):
        """
        check first condition: the warehouse has all product of order
        if has 1 candidate, return candidate, else check next condition
        :return:
        """
        next_candidates = []
        order_addr = order[self.ADDRESS]
        for i in candidates:
            if order_addr == i[self.ADDRESS]:
                next_candidates.append(i)
        print(f'#1 {next_candidates}')
        if 1 == len(next_candidates):
            return next_candidates
        else:
            # next condition
            return self.__check_second_condition(next_candidates, order)

    @exception_logging
    def __check_second_condition(self, candidates, order):
        """
        check second condition: the warehouse has all product of order
        :return:
        """
        next_candidates = []
        for ware_house in candidates:
            is_add = True
            for name, quality in order[self.ITEMS].items():
                if 0 == quality:
                    continue
                if not ware_house.get(self.ITEMS, {}).get(name, 0):
                    is_add = False
            if is_add:
                next_candidates.append(ware_house)
        print(f'#2 {next_candidates}')
        if candidates and not next_candidates:
            return candidates[0]
        if 1 == len(next_candidates):
            return next_candidates
        else:
            # next condition
            return self.__check_third_condition(next_candidates, order)

    @exception_logging
    def __check_third_condition(self, candidates, order):
        """
        check the warehouse has the largest quantity of product.
        :return:
        """
        max_stock = 0
        ware_house_candidate = {}
        for ware_house in candidates:
            for name, quality in order[self.ITEMS].items():
                if 0 == quality:
                    continue
                if ware_house.get(self.ITEMS, {}).get(name, 0):
                    if ware_house[self.ITEMS][name] > max_stock:
                        max_stock = ware_house[self.ITEMS][name]
                        ware_house_candidate = ware_house
        print(f'#3 {ware_house_candidate}')
        if not ware_house_candidate and candidates:
            return candidates[0]
        return ware_house_candidate

if __name__ == '__main__':
    sol = Sol()
    """ 
    Case 1
    """
    # sol.add_ware_house({Sol.WH_NAME: 'A', Sol.ADDRESS: ADDRESS.HANOI_ADDR, Sol.ITEMS: {Item.BOOK: 1}})
    # sol.add_ware_house({Sol.WH_NAME: 'B', Sol.ADDRESS: ADDRESS.HANOI_ADDR, Sol.ITEMS: {Item.BOOK: 3, Item.PEN: 3}})
    # sol.add_ware_house({Sol.WH_NAME: 'C', Sol.ADDRESS: ADDRESS.HANOI_ADDR, Sol.ITEMS: {Item.BOOK: 10, Item.PEN: 7}})
    # sol.add_ware_house({Sol.WH_NAME: 'D', Sol.ADDRESS: ADDRESS.HCM_ADDR, Sol.ITEMS: {Item.BOOK: 30, Item.PEN: 70}})
    """
    Case 2
    """
    sol.add_ware_house({Sol.WH_NAME: 'A', Sol.ADDRESS: ADDRESS.HANOI_ADDR, Sol.ITEMS: {Item.BOOK: 1}})
    sol.add_ware_house({Sol.WH_NAME: 'B', Sol.ADDRESS: ADDRESS.HCM_ADDR, Sol.ITEMS: {Item.BOOK: 10}})
    sol.add_ware_house({Sol.WH_NAME: 'C', Sol.ADDRESS: ADDRESS.HANOI_ADDR, Sol.ITEMS: {Item.PEN: 5}})
    rs = sol.make_choose_ware_house({Sol.ADDRESS: ADDRESS.HANOI_ADDR, Sol.ITEMS: {Item.BOOK: 2, Item.PEN: 3}})
    print(f'# Result ware house and quality of item for order \n {rs}')
