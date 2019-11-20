package main

import (
    "fmt"
    "log"
    "net/http"
    "os"
    "net"
)

func handler(w http.ResponseWriter, r *http.Request) {
    ip, port, _ := net.SplitHostPort(r.RemoteAddr)
    log.Printf("Getting request from %s:%s", ip, port)
    
    hostname, _  := os.Hostname()
    ipaddress, _ := net.LookupHost(hostname)

    fmt.Fprintf(w, "hostname: %s\nip address: %s\n", hostname, ipaddress[0])
}

func main() {
    http.HandleFunc("/", handler)
    log.Fatal(http.ListenAndServe(":8080", nil))
}
