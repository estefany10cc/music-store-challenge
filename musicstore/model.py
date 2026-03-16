from collections import defaultdict
from datetime import datetime

class Transaction:
    SELL : int = 1
    SUPPLY : int = 2
    def __init__(self, type: int , copies: int):
        self.type : int = type
        self.copies : int = copies
        self.date : datetime = datetime.now()



class Disc:
    def __init__(self, sid: str, title: str, artist: str, sale_price: float, purchase_price: float, quantity: int):
        self.sid : str = sid
        self.title : str = title
        self.artist : str = artist
        self.sale_price : float = sale_price
        self.purchase_price : float = purchase_price
        self.quantity : int = quantity
        self.song_list: list[str]= []
        self.transactions : list[Transaction] = []

    def add_song(self, song: str):
        self.song_list.append(song)

    def sell(self, copies: int)-> bool:
        if copies > self.quantity:
            return False
        else:
            self.quantity -= copies
            self.transactions.append(Transaction(Transaction.SELL, copies))
            return True

    def supply(self, copies: int):
            self.quantity += copies
            self.transactions.append(Transaction(Transaction.SUPPLY, copies))
            return True

    def copies_sold(self)-> int:
        copies_suma = 0

        for transaction in self.transactions:
            if transaction.type == Transaction.SELL:
                copies_suma += transaction.copies
        return copies_suma


    def __str__(self) -> str:
        lista_song = ""
        for song in self.song_list:
            lista_song += f"{song}, "
        return f"SID: {self.sid}\nTitle: {self.title}\nArtist: {self.artist}\nSong List: {lista_song[:-2]}"

class MusicStore:
    def __init__(self):
        self.discs: dict[str, Disc]= {}

    def add_disc(self, sid: str, title: str, artist: str, sale_price: float, purchase_price: float, quantity: int):
        if sid not in self.discs:
            self.discs[sid] = Disc(sid, title, artist, sale_price, purchase_price, quantity)

    def search_by_sid(self, sid: str)-> Disc | None:
            return self.discs.get(sid, None)

    def search_by_artist(self, artist: str) -> list[Disc]:
        return [d for d in self.discs.values() if d.artist == artist]

    def sell_disc(self, sid: str, copies: int) -> bool:
        disc = self.search_by_sid(sid)
        if disc is None:
            return False

        return disc.sell(copies)

    def supply_disc(self, sid: str, copies: int) -> bool:
        disc = self.search_by_sid(sid)
        if disc is None:
            return False

        disc.supply(copies)
        return True

    def worst_selling_disc(self)-> Disc | None:
        if len(self.discs) == 0:
            return None
        copi= defaultdict(int)
        for disc in self.discs.values():
            for transaction in disc.transactions:
                if transaction.type == Transaction.SELL:
                    copi[disc] += transaction.copies
        return min(copi, key=copi.get)


