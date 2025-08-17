module your_project::DocumentVerification {
    use sui::object::Object;
    use sui::tx_context::TxContext;

    struct Fingerprint has key {
        value: vector<u8>
    }

    public fun store_fingerprint(ctx: &mut TxContext, fingerprint: vector<u8>) {
        let new_fingerprint = Fingerprint { value: fingerprint };
        ctx.transfer_object(new_fingerprint, ctx.sender());
    }
}
