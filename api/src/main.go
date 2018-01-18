package main

import (
	"net/http"
	"log"
	"github.com/julienschmidt/httprouter"
	"lib"
)

func main() {
	router := httprouter.New()
	router.GET("/code.:code", lib.ResponseCode)
	err := http.ListenAndServe("0.0.0.0:9001", router)
	if err != nil {
		log.Fatal("ListenAndServe: ", err)
	}
}
