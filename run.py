import subprocess
import re

package_id = "0x7f33f9703883bf57809dff9b2eb185348d701d58261faabb25ef621252d4012e"
module_name = "document_registry"  # Make sure this is correct!
function_name = "store_fingerprint"
owner_address = "0x100f338ec7e2df3575488edeadcb0b4766ba679191d3247eadfaa5d8bad59551"
fingerprint = "c636816a1f0705a629cfb84cc4b68e971411eae525a2330db51c99f1d36f3d2c"

# Convert document name and fingerprint to byte arrays
doc_name_bytes = f'"[{",".join(str(ord(c)) for c in "document.txt")}]"'
fingerprint_bytes = f'"[{",".join(str(ord(c)) for c in fingerprint)}]"'

# Construct the command
command2 = f"sui client call --package {package_id} --module {module_name} --function {function_name} --args {owner_address} {doc_name_bytes} {fingerprint_bytes} --gas-budget 50000000"
result2 = subprocess.run(command2, shell=True, capture_output=True, text=True, encoding= "utf-8")
print("STDOUT:\n", result2.stdout)
print("STDERR:\n", result2.stderr)

if result2.returncode == 0:
    print("Contract published successfully.")
else:
    print("Failed to publish contract.")

