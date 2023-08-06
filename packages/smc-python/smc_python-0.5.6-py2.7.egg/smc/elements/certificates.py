"""
Module to provide certificate services for various features such as
client server protection and TLS server protection.
"""
from smc.base.model import Element, ElementCreator

class TLSServerCredential(Element):
    """ 
    If you want to inspect TLS traffic for which an internal server is the
    destination, you must create a TLS Credentials element to store the
    private key and certificate of the server.

    The private key and certificate allow the firewall to decrypt TLS traffic
    for which the internal server is the destination so that it can be inspected.
    
    After a TLSServerCredential has been created, you must apply this to the
    engine performing decryption.
    
    TLS Server Credentials can be created and self signed for simple use::
    
        tls = TLSServerCredential.create(name='tlsserver', common_name='CN=myserver')
        tls.self_sign()
        
    Add list of TLS Credentials to an engine::
        
        engine = Engine('myengine')
        engine.add_tls_credential([tls])
        engine.update()
    """
    typeof = 'tls_server_credentials'
    
    def __init__(self, name, **meta):
        super(TLSServerCredential, self).__init__(name, **meta)
    
    @classmethod
    def create(cls, name, common_name, public_key_algorithm='rsa',
               signature_algorithm='rsa_sha_512', key_length=4096):
        """
        Create a certificate signing request. 
        
        :param str name: name of TLS Server Credential
        :param str rcommon_name: common name for certificate. An example
            would be: "CN=CommonName,O=Organization,OU=Unit,C=FR,ST=PACA,L=Nice".
            At minimum, a "CN" is required.
        :param str public_key_algorithm: public key type to use. Valid values
            rsa, dsa, ecdsa.
        :param str signature_algorithm: signature algorithm. Valid values
            dsa_sha_1, dsa_sha_224, dsa_sha_256, rsa_md5, rsa_sha_1, rsa_sha_256,
            rsa_sha_384, rsa_sha_512, ecdsa_sha_1, ecdsa_sha_256, ecdsa_sha_384,
            ecdsa_sha_512. (Default: rsa_sha_512)
        :param int key_length: length of key. Key length depends on the key
            type. For example, RSA keys can be 1024, 2048, 3072, 4096. See SMC
            documentation for more details.
        :raises CreateElementFailed: failed to create CSR
        :return: this csr request
        :rtype: TLSServerCredential
        """
        json = {
            'name': name,
            'info': common_name,
            'public_key_algorithm': public_key_algorithm,
            'signature_algorithm': signature_algorithm,
            'key_length': key_length,
            'certificate_state': 'initial'
        }
        from pprint import pprint
        pprint(json)
        return ElementCreator(cls, json)
    
    def certificate_state(self):
        """
        State of the certificate. Available states are 'request' and
        'certificate'. If the state is 'request', this represents a
        CSR and needs to be signed.
        
        :rtype: str
        """
        return self.data.get('certificate_state')
    
    def self_sign(self):
        """
        Self sign the certificate in 'request' state. 
        
        :raises ActionCommandFailed: failed to sign with reason
        """
        return self.send_cmd(
            resource='self_sign')
    
    def certificate_export(self):
        """
        Return the certificate as string text
        
        :rtype: str
        """
        result = self._request(
            resource='certificate_export').read()
        return result.content

    def certificate_import(self, certificate):
        #POST
        pass
    
    def private_key_import(self, private_key):
        #POST
        pass
    
    def intermediate_certificate_export(self):
        #GET
        pass
    
    def intermediate_certificate_import(self, certificate):
        #POST
        pass


class ClientProtectionCA(Element):
    typeof = 'tls_signing_certificate_authority'
    
    def __init__(self, name, **meta):
        super(ClientProtectionCA, self).__init__(name, **meta)
    
    @classmethod
    def create(cls, name):
        json = {
            'name': name}
        
        return ElementCreator(cls, json)    