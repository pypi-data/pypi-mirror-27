#!/bin/python
import roomai.common
from roomai.sevenking import SevenKingPokerCard

class SevenKingPublicState(roomai.common.AbstractPublicState):
    def __init__(self):
        super(SevenKingPublicState,self).__init__()
        self.__stage__            = None
        self.__num_players__      = None
        self.__showed_cards__     = None
        self.__num_showed_cards__ = None
        self.__num_keep_cards__   = None
        self.__num_hand_cards__   = None
        self.__is_fold__          = None
        self.__num_fold__         = None
        self.__license_action__   = None

    def __get_stage__(self):    return self.__stage__
    stage = property(__get_stage__, doc="There are two stages in SevenKing. In the first stage(stage = 0), the player gets the same number of the poker cards after he takes an action (throws some cards)."+
                                        "In the second stage (stage=1), the player doesn't get the supplement. The player who firstly throws all his hand cards is the winner. ")


    def __get_num_players__(self): return self.__num_players__
    num_players = property(__get_num_players__, doc="The number of players in this game")


    def __get_showed_cards__(self):
        if self.__showed_cards__ is None:
            return None
        return tuple(self.__showed_cards__)
    showed_cards = property(__get_showed_cards__, doc="The poker cards have been thrown by the players and are public to all now."
                                                      "For example, showed_cards = [roomai.sevenking.SevenKingPokerCards.lookup(\"A_Spade\"),roomai.sevenking.SevenKingPokerCards.lookup(\"3_Heart\")]")


    def __get_num_showed_cards__(self):
        return self.__num_showed_cards__
    num_showed_cards = property(__get_num_showed_cards__, doc="The number of showed poker cards")

    def __get_num_hand_cards__(self):
        if self.__num_hand_cards__ is None:
            return None
        return tuple(self.__num_hand_cards__)
    num_hand_cards = property(__get_num_hand_cards__, doc="The number of cards in different players. For example, num_hand_cards = [3,5,2] denotes the player0 has 3 poker cards, the player1 has 5 poker cards and the player2 has 2 poker cards")

    def __get_is_fold__(self):
        if self.__is_fold__ is None:
            return None
        return tuple(self.__is_fold__)
    is_fold = property(__get_is_fold__, doc="is_fold is an array of which player has take the fold action. For example, is_fold = [true,true,false] denotes the player0 and player1 have taken the fold action")


    def __get_num_fold__(self):
        return self.__num_fold__
    num_fold = property(__get_num_fold__, doc="The number of players who has taken the fold action")


    def __get_license_action__(self):
        return self.__license_action__
    license_action = property(__get_license_action__, doc="Generally, the player need takes an action with the same pattern as the license action. Unless the player takes an action at the beginning of a round")

    def __deepcopy__(self, newinstance = None, memodict={}):
        if  newinstance is None:
            newinstance = SevenKingPublicState()
        newinstance   = super(SevenKingPublicState,self).__deepcopy__(newinstance = newinstance)

        newinstance.__stage__ = self.stage
        newinstance.__num_players__ = self.num_players

        if self.showed_cards is None:
            newinstance.__showed_cards = None
        else:
            newinstance.__showed_cards = [card.__deepcopy__() for card in self.showed_cards]

        newinstance.__num_showd_cards__ = self.num_showed_cards
        newinstance.__num_keep_cards__  = self.num_keep_cards
        newinstance.__num_hand_cards__  = self.num_hand_cards
        if self.is_fold is None:
            newinstance.__is_fold__ = None
        else:
            newinstance.__is_fold__         = list(self.__is_fold__)
        newinstance.__num_fold__  = self.num_fold
        if self.license_action is None:
            newinstance.__license_action = None
        else:
            newinstance.self.__license_action__  = self.license_action

        return newinstance

class SevenKingPrivateState(roomai.common.AbstractPrivateState):
    '''
    The private state of SevenKing
    '''
    def __init__(self):
        super(SevenKingPrivateState,self).__init__()
        self.__keep_cards__   = []

    def __get_keep_cards__(self):
        return tuple(self.__keep_cards__)
    keep_cards = property(__get_keep_cards__, doc="The keep cards")

    def __deepcopy__(self, newinstance = None, memodict={}):
        if newinstance is None:
            newinstance = SevenKingPrivateState()
        newinstance                = super(SevenKingPrivateState,self).__deepcopy__(newinstance = newinstance)
        newinstance.__keep_cards__ =  [card.__deepcopy__() for card in self.keep_cards   ]
        return newinstance


class SevenKingPersonState(roomai.common.AbstractPersonState):
    '''
    The person state of SevenKing 
    '''
    def __init__(self):
        super(SevenKingPersonState,self).__init__()
        self.__hand_cards__         = []
        self.__hand_cards_keyset__  = set()
        self.__hand_cards_key__     = ""

    def __get_hand_cards__(self):
        return tuple(self.__hand_cards__)
    hand_cards = property(__get_hand_cards__, doc="The hand cards of the person state. For example, hand_cards = [roomai.sevenking.SevenKingPokerCard.lookup(\"A_Spade\")] ")

    def __get_hand_cards_key__(self):
        return self.__hand_cards_key__
    hand_cards_key = property(__get_hand_cards_key__, doc="The hand cards key of the person state. For example, hand_cards_key  = \"3_Spade,A_Spade\"")

    def __get_hand_cards_keyset__(self):
        return frozenset(self.__hand_cards_keyset__)
    hand_cards_keyset = property(__get_hand_cards_keyset__, doc = "The set of the poker cards' key in the hand cards. For example, hand_cards_keyset={\"A_Spade\"}")


    def __add_card__(self, c):
        self.__hand_cards__.append(c)
        self.__hand_cards_keyset__.add(c.key)

        for j in range(len(self.__hand_cards)-1,0,-1):
            if SevenKingPokerCard.compare(self.__hand_cards__[j - 1], self.__hand_cards__[j]) > 0:
                tmp = self.__hand_cards__[j]
                self.__hand_cards__[j] = self.__hand_cards__[j-1]
                self.__hand_cards__[j-1] = tmp
            else:
                break

        self.__hand_cards_key = ",".join([c.key for c in self.__hand_cards__])

    def __add_cards__(self, cards):
        len1 = len(self.__hand_cards__)
        for c in cards:
            self.__hand_cards__.append(c)
            self.__hand_cards_keyset__.add(c.key)
        len2 = len(self.__hand_cards__)


        for i in range(len1,len2-1):
            for j in range(i,0,-1):
                if SevenKingPokerCard.compare(self.__hand_cards__[j-1], self.__hand_cards__[j]) > 0:
                    tmp      = self.__hand_cards__[j]
                    self.__hand_cards__[j] = self.__hand_cards__[j-1]
                    self.__hand_cards__[j-1] = tmp
                else:
                    break


        #self.__hand_cards.sort(cmp=SevenKingPokerCard.compare)
        self.__hand_cards_key__ = ",".join([c.key for c in self.__hand_cards__])



    def __del_card__(self, c):
        self.__hand_cards_keyset__.remove(c.key)

        tmp = self.__hand_cards__
        self.__hand_cards__ = []
        for i in range(len(tmp)):
            if c.key == tmp[i].key:
                continue
            self.__hand_cards__.append(tmp[i])
        self.__hand_cards_key__ = ",".join([c.key for c in self.__hand_cards__])


    def __del_cards__(self, cards):
        for c in cards:
            self.__hand_cards_keyset__.remove(c.key)

        tmp = self.__hand_cards__
        self.__hand_cards__ = []
        for i in range(len(tmp)):
            if tmp[i].key not in self.__hand_cards_keyset__:
                continue
            self.__hand_cards__.append(tmp[i])
        self.__hand_cards_key__ = ",".join([c.key for c in self.__hand_cards__])

    def __gen_pointrank2cards__(self):
        if self.__hand_cards_key__ in AllPointRank2Cards:
            return AllPointRank2Cards[self.__hand_cards_key__]
        else:
            point2cards = dict()
            for c in self.hand_cards:
                pointrank = c.point_rank
                if pointrank not in point2cards:
                    point2cards[pointrank] = []
                point2cards[pointrank].append(c)
            for p in point2cards:
                for i in range(len(point2cards[p])-1):
                    for j in range(i+1,len(point2cards[p])):
                        if SevenKingPokerCard.compare(point2cards[p][i],point2cards[p][j]) > 0:
                            tmp = point2cards[p][i]
                            point2cards[p][i] = point2cards[p][j]
                            point2cards[p][j] = tmp
                #point2cards[p].sort(cmp=SevenKingPokerCard.compare)

            AllPointRank2Cards[self.__hand_cards_key__] = point2cards
            return point2cards

    def __deepcopy__(self, memodict={}, newinstance = None):
        if newinstance is None:
            newinstance          = SevenKingPersonState()
        newinstance      = super(SevenKingPersonState, self).__deepcopy__(newinstance= newinstance)
        newinstance.__hand_cards__           = list(tuple(self.__hand_cards__))
        newinstance.__hand_cards_set__       = set(self.__hand_cards_keyset__)
        newinstance.__hand_cards_key__       = self.__hand_cards_key__
        return newinstance



AllPointRank2Cards = dict()
