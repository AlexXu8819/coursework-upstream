"""
CMSC 14200, Winter 2024
Homework #1

People Consulted:
   List anyone (other than the course staff) that you consulted about
   this assignment.

Online resources consulted:
   List the URLs of any online resources other than the course text and
   the official Python language documentation that you used to complete
   this assignment.
"""

from typing import Optional
from abc import ABC, abstractmethod
from tree import TreeNode


def count_words(list_of_strings: list[str], starts_with: str) -> dict[str, int]:
    """
    Find the words that start with a given substring and count the number of
    times each word appears.

    Inputs:
        list_of_strings (list): the list of words
        starts_with (string): substring that has to appear in each word

    Returns (dict): the words and counts of each word that starts with the given
    """
    count_dict = {}
    for i in range(len(list_of_strings)):
        if(list_of_strings[i].startswith(starts_with)):
            if(list_of_strings[i] in count_dict):
                count_dict[list_of_strings[i]] += 1
            else:
                count_dict[list_of_strings[i]] = 1
    return count_dict
    raise NotImplementedError("todo: count_words")


class Board:
    """
    Class to represent a game board.

    Attributes:
        rows (int): number of rows
        cols (int): number of columns
        board (list): the game board
        location_of_pieces (dictionary): the location of each piece on the board

    Methods:
        add_piece: add a piece represented by a string to the board
    """

    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.board = [[None] * cols for _ in range(rows)]
        self.location_of_pieces = {}

    def add_piece(self, piece, location):
        """
        Add a piece represented by a string to the board.

        Inputs:
            piece (string): the piece to add
            location (tuple): the (row, column) location of where to add
                the piece

        Returns (bool): True if the piece was added successfully,
            False otherwise
        """
        row, col = location

        if self.board[row][col] is None:
            self.board[row][col] = piece
            if piece in self.location_of_pieces:
                self.location_of_pieces[piece].append(location)
            else:
                self.location_of_pieces[piece] = [location]
            return True
        return False


def get_all_paths(t: TreeNode) -> list[list[int]]:
    """
    Find all the unique paths from the root to a leaf node in a tree.

    Inputs:
        t (TreeNode): the tree

    Returns (list): the list of paths
    """
    if(t.is_leaf()):
        return [[t.value]]
    
    paths = []
    for i in range(len(t.children)):
        child_paths = get_all_paths(t.children[i])
        for pat in child_paths:
            paths.append([t.value] + pat)
    
    return paths
    
    raise NotImplementedError("todo: get_all_paths")
class CannotBeNegative(Exception):
    
    pass

class InsufficientFundsError(Exception):
    """
    Exception to be raised when an account has insufficient funds
    """
    pass

class Account(ABC):
    """
    Class to represent a bank account.

    Methods:
        deposit: deposit money into the account
        withdraw: withdraw money from the account

    Property:
        balance: the balance of the account
    """
    def __init__(self, account_number: int, balance: float = 0):
        self._account_number = account_number
        if(balance < 0):
            raise CannotBeNegative("Balance can't be negative")
        self._balance = float(balance)

    def deposit(self, amount: float) -> None:
        """
        Makes a deposit in the account.

        Inputs:
            amount (float): Amount to deposit

        Returns: Nothing
        """
        if(amount < 0):
            raise CannotBeNegative("Amount can't be negative")
        self._balance += amount
        return None

    def withdraw(self, amount: float) -> float:
        """
        Makes a withdrawal from the account.

        Inputs:
            amount (float): Amount to withdraw

        Returns (float): Withdrawn amount.
        """
        if amount < 0:
            raise CannotBeNegative("Amount can't be negative")
        
        if amount > self._balance:
            raise InsufficientFundsError("Not enough funds in balance to withdraw")

        
        self._balance -= amount
        return amount
    
    @property
    def balance(self) -> float:
        """
        Returns the balance of the account

        Returns (float): Account balance
        """
        return self._balance

class SavingsAccount(Account):

    """
    Class to represent a savings account
    """
    def deposit(self, amount):
        if(amount < 0):
            raise CannotBeNegative("Amount can't be negative")
        self._balance += amount
    
    def withdraw(self, amount):
        if(amount < 0):
            raise CannotBeNegative("Amount can't be negative")
        if(amount > self._balance):
            raise InsufficientFundsError("Not enough money in account")

        self._balance -= amount

        return amount

class CheckingAccount(Account):
    """
    Class to represent a checking account
    """

    def __init__(self, account_number, balance, overdraft):
        super().__init__(account_number, balance)
        if(overdraft < 0):
            raise CannotBeNegative("Can't be negative overdraft")
        self._available_overdraft = overdraft
        self._overdraft_limit = overdraft
    
    @property
    def balance(self):
        return self._balance
    
    def withdraw(self, amount):
        if(amount < 0):
            raise CannotBeNegative("Amount can't be negative")
        if(amount > self._available_overdraft + self._balance):
            raise InsufficientFundsError("Not enough funds to withdraw")
        if(amount < self._balance):
            self._balance -= amount
            return amount
        
        gap = amount - self._balance
        self._balance = 0
        self._available_overdraft -= gap
        return amount
    
    def deposit(self, amount):
        if(amount < 0):
            raise CannotBeNegative("Amount can't be negative")
        gap = min(amount, self._overdraft_limit - self._available_overdraft)

        self._available_overdraft += gap
        self._balance += amount - gap

class HighYieldSavingsAccount(SavingsAccount):
    """
    Class to represent a high yeild savings account
    """
    def __init__(self, account_number, balance, min_balance, interest_rate):
        super().__init__(account_number, balance)
        if(min_balance < 0 or interest_rate < 0):
            raise CannotBeNegative("Minimum balance and interest rate can't be negative")
        self._min_balance = min_balance
        self._interest_rate = interest_rate
    
    def add_monthly_interest(self):
        self._balance = self._balance + (self._interest_rate * self._balance)

    def withdraw(self, amount):
        if(self._balance - amount < self._min_balance):
            raise InsufficientFundsError("Can't drop below minimum account balance")
        
        return super().withdraw(amount)
        

