const CLIENT_ID = '9d88e28b87f74a918458fad03748a14d'
const REDIRECT_URI = "http://localhost:8888/callback"
const CLIENT_SECRET = '6661ad45ea274f96bb536799d6b76127'

//var SpotifyWebApi = require('spotify-web-api-node')

// When page is loaded, ask user for login 
$(document).ready(function() {
    //clientCredentialsFlow()
    //const accessToken = promptForLogin()    
    //useAccessToken(accessToken)
    //authorizationCodeFlow()
    implicitGrantFlow()
})

// Implicit Grant Flow 
function implicitGrantFlow() {
    $.ajax({
        url: "https://accounts.spotify.com/authorize",
        data: {
            client_id: CLIENT_ID,
            response_type: "token",
            redirect_uri: REDIRECT_URI,
            scope: "user-library-read"
        },
        success: function(result) {console.log("Success!\n", result)},
        error: function(error) {console.log("FUCK")},
    })
}


// Attempt at getting Client Credientials Flow to work - no luck 
function clientCredentialsFlow() {
    $.ajax({
        type: "POST",
        url: "https://accounts.spotify.com/api/token",
        data: {
            grant_type: "client_credentials"
        },
        header: {
            'Authorization': "Basic " + (CLIENT_ID + ':' + CLIENT_SECRET).toString('base64')
        },
        mode: 'cors'
    })
}

// Prompts user to log in to spotify 
async function promptForLogin() {
    
    /* // Trying to see if using fetch instead of jQuery makes any difference 
    const result = await fetch(`https://accounts.spotify.com/authorize?client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&scope=user-library-read&response_type=token`)
    console.log(result)
    */

    $.ajax({ 
        //url: `https://accounts.spotify.com/authorize?client_id=${CLIENT_ID}&redirect_uri=${REDIRECT_URI}&scope=user-library-read&response_type=token`,
        
        url: "https://accounts.spotify.com/authorize",
        data: {
            client_id: CLIENT_ID,
            redirect_uri: "http://localhost:8888/callback", // Listed as the redirect uri 
            response_type: "token",
        }, 
        credentials: 'include',
        success: function(result) {
            console.log("success!\n", result) },
        error: function(error) {
            console.log("FUCK")
        }
    })
}

// First step of Authorization Code Flow (1st on listed flows on doc page)
function authorizationCodeFlow() {
    $.ajax({
        url: 'https://accounts.spotify.com/authorize',
        data: {
            client_id: CLIENT_ID,
            response_type: 'code', 
            redirect_uri: REDIRECT_URI,
        }
    })
}
