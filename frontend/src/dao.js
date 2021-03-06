/*
 Copyright 2020 Skye Isard

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
*/
import axios from 'axios'
import Vue from 'vue'


function post(path, payload, resultHandlerFn, errorHandlerFn) {
    axios.post(path, payload, {
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": Vue.$cookies.get('csrftoken')
        }  
    }).then(resultHandlerFn).catch(errorHandlerFn)
}

export default {

    isAuthenticated(resultHandlerFn, errorHandlerFn) {
        post('/is_authenticated/', {}, resp => resultHandlerFn(resp.data.authenticated), errorHandlerFn)
    },

    authenticate(username, password, successFn, errorFn) {
        post('/authenticate/', {username, password}, successFn, errorFn)
    },

    logout(successFn, errorFn) {
        post('/logout/', {}, successFn, errorFn)
    },

    changePassword(oldPassword, newPassword, successFn, errorFn) {
        post('/change_password/', {oldPassword, newPassword}, successFn, errorFn)
    },
/*
    getLobbyData() {

    }

    createNewGame(settings) {

    }
*/

    subscribeToClubList() {
        const protocol = location.protocol === 'https:' ? 'wss://' : 'ws://'
        return new WebSocket(protocol + location.host + '/ws/clublist/')
    }
        

    /*subscribeToGameMessages(handlerFn) {*/
    /**/ 
    /*} // */
        
}
