import certifi
import urllib3
import json

from config import TWBotConfig as conf


class BattleNetApi(object):

    def __init__(self):
        self.token = None
        self.unauth_error = False
        self.http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',
                                        ca_certs=certifi.where())

    def request_json(self, url):
        r = self.http.request('GET', url)
        if r.status == 401:
            self.unauth_error = True
            return False
    
        return json.loads(r.data.decode('utf-8'))

    def get_token(self):
        if self.token is None or force:
            token_url = f"https://{conf.region}.battle.net/"
            token_url += f"oauth/token?grant_type=client_credentials"
            token_url += f"&client_id={conf.BATTLE_KEY}"
            token_url += f"&client_secret={conf.BATTLE_SECRET}"

            j = self.request_json(token_url)
            self.token = j["access_token"]
        
        return self.token
    
    def get_affix(self):
        affix_list = []

        url = f"https://{conf.region}.api.battle.net/"
        url += f"data/wow/mythic-challenge-mode/"
        url += f"?namespace=dynamic-{conf.region}"
        url += f"&locale={conf.locale}"
        url += f"&access_token={self.get_token()}"

        j = self.request_json(url)

        current_affix = j['current_keystone_affixes']

        for a in current_affix:
            starting_level = int(a['starting_level'])
            name = a['keystone_affix']['name']
            affix_list.append([starting_level, name])

        return sorted(affix_list, key=lambda x: x[0])

        # Alternative
        """
        url = f"https://raider.io/api/v1/mythic-plus/affixes?region={conf.region}"
        r = self.http.request('GET', url)
        print(r.data)

        j = self.request_json(url)
        
        for k in j:
            print(f"{k}: {j[k]}")
            print()
        """

if __name__ == "__main__":
    api = BattleNetApi()
    api.get_affix()