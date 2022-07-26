# NOTE: As of 2022-06-01 the GitLab Enterprise Edition License has the following
# section:
#   Notwithstanding the foregoing, you may copy and modify the Software for development
#   and testing purposes, without requiring a subscription.
#
# https://gitlab.com/gitlab-org/gitlab/-/blob/29503bc97b96af8d4876dc23fc8996e3dab7d211/ee/LICENSE
#
# This code is strictly intended for use in the testing framework of python-gitlab

# Code inspired by MIT licensed code at: https://github.com/CONIGUERO/gitlab-license.git

require 'openssl'
require 'gitlab/license'

# Generate a 2048 bit key pair.
license_encryption_key = OpenSSL::PKey::RSA.generate(2048)

# Save the private key
File.open("/.license_encryption_key", "w") { |f| f.write(license_encryption_key.to_pem) }
# Save the public key
public_key = license_encryption_key.public_key
File.open("/.license_encryption_key.pub", "w") { |f| f.write(public_key.to_pem) }
File.open("/opt/gitlab/embedded/service/gitlab-rails/.license_encryption_key.pub", "w") { |f| f.write(public_key.to_pem) }

Gitlab::License.encryption_key = license_encryption_key

# Build a new license.
license = Gitlab::License.new

license.licensee = {
  "Name"    => "python-gitlab-ci",
  "Company" => "python-gitlab-ci",
  "Email"   => "python-gitlab-ci@example.com",
}

# The date the license starts. 
license.starts_at         = Date.today
# Want to make sure we get at least 1 day of usage. Do two days after because if CI
# started at 23:59 we could be expired in one minute if we only did one next_day.
license.expires_at         = Date.today.next_day.next_day

# Use 'ultimate' plan so that we can test all features in the CI
license.restrictions = {
  :plan => "ultimate", 
  :id   => rand(1000..99999999)
}

# Export the license, which encrypts and encodes it.
data = license.export

File.open("/python-gitlab-ci.gitlab-license", 'w') { |file| file.write(data) }
