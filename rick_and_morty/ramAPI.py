import requests

class ramAPI:
    def __init__(self, base_url="https://rickandmortyapi.com/api/") -> None:
        self.urls = {
            "base"      : base_url,
            "character" : base_url+"character/",
            "location"  : base_url+"location/",
            "episode"   : base_url+"episode/"
        }

    def get_all(self, get_type="base", page='base') -> dict:      
        if get_type not in self.urls.keys():
            print(f"{get_type} is not a valid query type")
            return 1  
        
        if page == 'base':
            return requests.get(self.urls[get_type]).json()
        else:
            return requests.get(page).json()
        
    def schema(self, get_type="base", grab='results') -> list:
        if get_type not in self.urls.keys():
            print(f"{get_type} is not a valid query type")
            return 1 

        tmp = requests.get(self.urls[get_type]).json()
        
        if get_type == "base":
            return list(tmp.keys())
        else:
            return list(tmp[grab][0].keys())

    def get_id(self,get_type='character', id=None) -> str:
        if id == None:
            print("You need to pass an id")
            return
        return requests.get(self.urls[get_type]+str(id)).json()

    def getNameByID(self, get_type='character', id=None) -> str:
        return self.get_id(get_type, id)['name']

    def query(self, get_type="base", **kwargs) -> dict:
        if get_type not in self.urls.keys():
            print(f"{get_type} is not a valid query type")
            return 1
        query_url = self.urls[get_type] + "?"
        query_dt = []
        for val in kwargs:
            if kwargs[val] == "ignore":
                continue
            query_dt.append(f"{val}={kwargs[val]}")
        query_dt = "&".join(query_dt)
        return requests.get(query_url + query_dt).json()

if __name__ == "__main__":
    base_url = "https://rickandmortyapi.com/api/"
    ram = ramAPI(base_url)
    print(ram.get_all('character')['info'])