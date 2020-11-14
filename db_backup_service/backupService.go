package main

import (
	"encoding/json"
	"fmt"
	"io"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strings"

	"github.com/imroc/req"
)

const authFile = "./authentication.json"
const tokensFile = "./tokens.json"
const dbFile = "../db/tracks.db"
const uploadPath = "/moodify/db_backup/tracks.db"

var logFile, err = os.OpenFile("./logs.txt", os.O_APPEND|os.O_CREATE|os.O_WRONLY, os.ModePerm)
var writers = io.MultiWriter(os.Stdout, logFile)
var logger = log.New(writers, "", log.LstdFlags)

func getAuthCredentials() (string, string) {

	authFile, err := os.Open(authFile)
	if err != nil {
		logger.Println(err)
	}
	if err == os.ErrNotExist {
		logger.Println("Authentication file does not exist!")
		logger.Println("Create authentication.json first with the app key and app secret")

		os.Exit(1)
	}
	defer authFile.Close()

	byteValue, _ := ioutil.ReadAll(authFile)

	var auth map[string]string
	json.Unmarshal(byteValue, &auth)

	return auth["APP_KEY"], auth["APP_SECRET"]
}

func responseToMap(response *req.Resp) map[string]interface{} {
	// turning response into a map
	var m map[string]interface{}
	err := response.ToJSON(&m)
	if err != nil {
		logger.Println(err)
	}

	return m
}

func getFirstTokens() {
	appKey, appSecret := getAuthCredentials()
	tokenURL := "https://api.dropboxapi.com/oauth2/token"

	body := req.Param{
		"code":          "vQlHyEq-NC4AAAAAAAAAi0Xx9wD3W0kkQN656ZvAgko",
		"grant_type":    "authorization_code",
		"client_id":     appKey,
		"client_secret": appSecret,
	}

	tokenRes, err := req.Post(tokenURL, body)
	if err != nil {
		logger.Println(err)
	}

	jsonResponse := responseToMap(tokenRes)

	// extracting tokens from response
	accessToken := jsonResponse["access_token"].(string)
	refreshToken := jsonResponse["refresh_token"].(string)

	// creating new map with the tokens
	tokens := map[string]string{
		"ACCESS_TOKEN":  accessToken,
		"REFRESH_TOKEN": refreshToken,
	}

	logger.Println("Got tokens:", tokens)

	updateTokensFile(tokens)
}

func getTokensFromFile() (string, string) {
	tokenFile, err := os.Open(tokensFile)
	if err != nil {
		logger.Println(err)
	}
	if err == os.ErrNotExist {
		logger.Println("Tokens file does not exist!")
		logger.Println("Run getFirstTokens() with a valid authorization code to create tokens file")

		os.Exit(1)
	}
	defer tokenFile.Close()

	byteValue, _ := ioutil.ReadAll(tokenFile)

	var tokens map[string]string
	json.Unmarshal(byteValue, &tokens)

	return tokens["ACCESS_TOKEN"], tokens["REFRESH_TOKEN"]
}

func updateTokensFile(newTokens map[string]string) {
	// writing tokens into tokens.json
	tokensFile, err := os.OpenFile(tokensFile, os.O_WRONLY|os.O_CREATE, os.ModePerm)
	if err != nil {
		logger.Println(err)
	}
	defer tokensFile.Close()

	encoder := json.NewEncoder(tokensFile)
	encoder.Encode(newTokens)
}

func validToken(accessToken string) bool {
	// check if token is expired
	checkHeader := req.Header{
		"Authorization": fmt.Sprintf("Bearer %s", accessToken),
		"Content-Type":  "application/json",
	}

	body := map[string]string{
		"query": "test",
	}

	res, err := req.Post("https://api.dropboxapi.com/2/check/user", checkHeader, req.BodyJSON(&body))
	if err != nil {
		logger.Println(err)
	}

	return res.Response().StatusCode == 200
}

func requestNewToken() {
	_, refreshToken := getTokensFromFile()
	appKey, appSecret := getAuthCredentials()

	tokenURL := "https://api.dropbox.com/oauth2/token"

	requestBody := req.Param{
		"grant_type":    "refresh_token",
		"refresh_token": refreshToken,
		"client_id":     appKey,
		"client_secret": appSecret,
	}

	res, err := req.Post(tokenURL, requestBody)
	if err != nil {
		logger.Println(err)
	}

	jsonResponse := responseToMap(res)

	// extracting tokens from response
	accessToken := jsonResponse["access_token"].(string)

	// creating new map with the tokens
	tokens := map[string]string{
		"ACCESS_TOKEN":  accessToken,
		"REFRESH_TOKEN": refreshToken,
	}

	logger.Println("Got new access token:", accessToken)

	updateTokensFile(tokens)
}

func uploadDBFile(accessToken string) {
	uploadURL := "https://content.dropboxapi.com/2/files/upload"

	file, err := os.Open(dbFile)
	if err != nil {
		logger.Println(err)
	}

	client := &http.Client{}
	req, err := http.NewRequest("POST", uploadURL, file)
	req.Header.Set("Content-Type", "application/octet-stream")
	req.Header.Set("Authorization", fmt.Sprintf("Bearer %s", accessToken))
	req.Header.Set("Dropbox-API-Arg", fmt.Sprintf("{\"path\": \"%s\", \"mode\": \"overwrite\", \"mute\": true}", uploadPath))

	_, err = client.Do(req)
	if err != nil {
		logger.Println(err)
		logger.Fatalln("Error uploading file to dropbox")
	}

	logger.Println("Successfully uploaded db file!")
}

func getUploadedFileSize(accessToken string) {
	url := "https://api.dropboxapi.com/2/files/get_metadata"

	client := &http.Client{}
	req, err := http.NewRequest("POST", url)
	req.Header.Set("Content-Type", "application/json")
	req.Header.Set("Authorization", fmt.Sprintf("Bearer %s", accessToken))
	
	body := map[string]string{
		"path": uploadPath
	}
	req.BodyJSON(&body)

	res, err := client.Do(req)
	logger.Println(res)
}

func main() {
	accessToken, refreshToken := getTokensFromFile()

	logger.Println(strings.Repeat("*", 20))
	logger.Println("Tokens successfully read from file")
	logger.Println()
	logger.Println("Access Token:", accessToken)
	logger.Println("Refresh Token:", refreshToken)
	logger.Println(strings.Repeat("*", 20))

	// checking if token is still valid and requesting a new
	// one if not
	if !validToken(accessToken) {
		logger.Println("Access token is invalid!")
		logger.Println("Requesting new access token...")
		requestNewToken()
	}

	uploadDBFile(accessToken)
}
