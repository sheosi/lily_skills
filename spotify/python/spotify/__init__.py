import os
from typing import Optional
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from lily_ext import action, answer, conf, translate

@action(name = "spotify")
class Spotify:

    def __init__(self):
        os.system("systemctl --user start spotifyd")

        scope = "user-library-read user-read-playback-state streaming"
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                scope=scope,
                client_id=conf("client_id"),
                client_secret=conf("secret"),
                redirect_uri="http://localhost",
                username=conf("username")
            )
        )
        

    def get_dev(self) -> Optional[str]:
        dev = self.get_dev_all()
        if not dev is None:
            return dev["id"]
        else: return None

    def get_dev_all(self) -> Optional[dict]:
        results = self.sp.devices()
        for dev in results["devices"]:
            if dev["name"].startswith("Spotifyd"):
                return dev
             
        return None

    def trigger_action(self, context):
        if context["intent"] == "play_track":
            dev = self.get_dev()
            if not dev is None:
                str_input = context["track_name"]
                search_res = self.sp.search(str_input, limit=1, offset=0, type='track', market=None)["tracks"]["items"]
                if search_res:
                    track_uri = search_res[0]["uri"]
                    self.sp.start_playback(device_id=dev, context_uri=None, uris=[track_uri], offset=None, position_ms=None)
                    return answer(translate("on_music_play",context), context)
                else:
                    return answer(translate("on_song_no_found",context), context)
            
            else:
                return answer(translate("on_no_dev", context), context)
        
        if context["intent"] == "stop_track":
            dev = self.get_dev()
            if not dev is None:
                self.sp.pause_playback(device_id=dev)
                return answer(translate("on_music_stop",context), context)
            else:
                return answer(translate("on_no_dev", context), context)
        
        if context["intent"] == "lower_volume":
            dev = self.get_dev()
            if not dev is None:
                self.sp.pause_playback(device_id=dev)
                return answer(translate("on_lower_volume",context), context)
            else:
                return answer(translate("on_no_dev", context), context)
    
