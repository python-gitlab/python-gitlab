# list
msgs = gl.broadcastmessages.list()
# end list

# get
msg = gl.broadcastmessages.get(msg_id)
# end get

# create
msg = gl.broadcastmessages.create({'message': 'Important information'})
# end create

# update
msg.font = '#444444'
msg.color = '#999999'
msg.save()
# end update

# delete
gl.broadcastmessages.delete(msg_id)
# or
msg.delete()
# end delete
