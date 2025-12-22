# https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html#programmatically-creating-a-personal-access-token

user = User.find_by_username('root')

token = user.personal_access_tokens.first_or_create(scopes: ['api', 'sudo'], name: 'default', expires_at: 365.days.from_now);
token.set_token('glpat-python-gitlab-token_');
token.save!

puts token.token
