FROM golang as builder
COPY web.go .
RUN GOOS=linux GOARCH=386 go build -a ./web.go

FROM scratch
COPY --from=builder /go/ /go/
EXPOSE 8080
CMD ["/go/web"]
