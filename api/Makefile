CERTIFICATES_FOLDER = ca-certificates
CERTIFICATES_PREFIX = object-cut

.PHONY: all
all: ca-certificates

.PHONY: clean
clean:
	- rm $(CERTIFICATES_FOLDER)/$(CERTIFICATES_PREFIX).*

#######################################################################
# OpenSSL: Generate certificates
#######################################################################

.PHONY: ca-certificates
ca-certificates: $(CERTIFICATES_FOLDER)/$(CERTIFICATES_PREFIX).key $(CERTIFICATES_FOLDER)/$(CERTIFICATES_PREFIX).crt

.PRECIOUS: %.key
%.key:
	openssl genrsa \
		-out $@ \
		2048

.PRECIOUS: %.csr
%.csr: %.key
	openssl req \
		-subj \
		"/C=ES/ST=Barcelona/L=Barcelona/O=AlbertSuarezOrg/CN=alsumo95@gmail.com" \
		-new -key $< \
		-out $@

.PRECIOUS: %.crt
%.crt: %.csr %.key
	openssl x509 \
		-req -days 365 \
		-in $*.csr \
		-signkey $*.key \
		-out $@
