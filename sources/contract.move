module doc_auth::document_registry {

    /// Struct to store document fingerprint
    public struct Document has key, store {
        id: UID, // Unique ID required by Sui
        owner: address,
        name: vector<u8>,
        fingerprint: vector<u8>,
    }

    /// Store the fingerprint on the blockchain
    public entry fun store_fingerprint(
        owner: address,
        name: vector<u8>,
        fingerprint: vector<u8>,
        ctx: &mut TxContext
    ) {
        let doc = Document {
            id: object::new(ctx), // Corrected UID generation
            owner,
            name,
            fingerprint,
        };

        transfer::transfer(doc, owner); // Store object on-chain
    }

    /// Retrieve the stored fingerprint using object reference
    public fun get_fingerprint(doc: &Document): (vector<u8>, vector<u8>) {
        (doc.name, doc.fingerprint)
    }
}
