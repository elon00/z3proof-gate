// The original Rust executable printed fabricated RPC/PQC/100/100 assertions.
// Fail closed rather than implying that this binary verifies a protocol.
fn main() {
    eprintln!("Rust Z3 gate is not implemented. Use the offline Python Z3 verifier and its real regression tests.");
    std::process::exit(2);
}
