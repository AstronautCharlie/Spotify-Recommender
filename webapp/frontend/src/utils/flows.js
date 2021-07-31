<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js" type="text/javascript"></script>

// Execute authorizationCodeFlow initial request. Should receive an authorization code upon successful authentication that can be used 
// to obtain an access token.
export function authorizationCodeFlow(url, data, callback) {
    url = buildRequestURI(url, data)
    fetch(url, {
        mode: 'cors',
        headers: {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Headers": "Origin, X-Requested-With, Content-Type, Accept"
          }
    })
    .then(callback)
    
}

// helper function to build URI. Can be expanded to handle all types of flows
function buildRequestURI(url, data) {
    return url + "?client_id=" + data.client_id + "&redirect_uri=" + data.redirect_uri + "&scope=" + data.scope + "&response_type=" + data.response_type
}










// function implicitGrantFlow(url, data) {
//     $.ajax({
//         url: "https://accounts.spotify.com/authorize",
//         data: {
//             client_id: CLIENT_ID,
//             response_type: "token",
//             redirect_uri: REDIRECT_URI,
//             scope: "user-library-read"
//         },
//         success: function(result) {console.log("Success!\n", result)},
//         error: function(error) {console.log("FUCK")},
//     })
// }


// // Attempt at getting Client Credientials Flow to work - no luck 
// function clientCredentialsFlow(url, data) {
//     $.ajax({
//         type: "POST",
//         url: "https://accounts.spotify.com/api/token",
//         data: {
//             grant_type: "client_credentials"
//         },
//         header: {
//             'Authorization': "Basic " + (CLIENT_ID + ':' + CLIENT_SECRET).toString('base64')
//         },
//         mode: 'cors'
//     })
// }