# https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html#programmatically-creating-a-personal-access-token

user = User.find_by_username('root')

token = user.personal_access_tokens.create(scopes: [:api, :sudo], name: 'default');
token.set_token('python-gitlab-token');
token.save!

puts token.token
