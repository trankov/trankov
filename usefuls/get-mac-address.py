import uuid

mc = hex(uuid.getnode())[2:]
mc = ":".join([mc[i : i + 2] for i in range(0, len(mc), 2)])

print(mc)
