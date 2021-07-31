import logo from './logo.svg';
import './App.css';
import {authorizationCodeFlow} from './utils/flows'

function App() {

  // flow type to use with API call
  const FLOW_TYPE = "authorizationCode"

  // parameters for API call
  const CLIENT_ID = 'd2315b62f2014f4bafba23159d105d51'
  const REDIRECT_URI = "http://localhost:3000"
  const CLIENT_SECRET = null
  const SCOPES = "user-library-read"
  const RESPONSE_TYPE = "token"
  const SHOW_DIALOG = "true"

  // URIs for each respective flow
  const AUTHORIZATION_CODE_FLOW_URI = "https://accounts.spotify.com/authorize"

  // function to execute on click for "Log In here"
  const initFlow = (flowType) => {
    switch (flowType) {
      case "authorizationCode":
        var data = {
          client_id: CLIENT_ID,
          response_type: RESPONSE_TYPE, 
          redirect_uri: REDIRECT_URI,
          scope: SCOPES
        }
        // imported from flows.js
        authorizationCodeFlow(AUTHORIZATION_CODE_FLOW_URI, data, (resp) => console.log(resp))
        break;
      case "clientCredentials":
        break;
      case "implicitGrant":
        break;
    }
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>Spotify Datify</h1>
        <button onClick={() => initFlow(FLOW_TYPE)}>Log In here</button>
            <div className="search">
                <form>
                    <label for="searchterm">Enter an artist or album</label>
                    <input type="text" id="searchterm"/>
                    <input type="button" value="Submit"/>
                </form>
                <div className="searchresults">
                </div>
            </div>
      </header>
    </div>
  );
}

export default App;
