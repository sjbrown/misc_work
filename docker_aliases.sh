alias d.images='docker images --format "{{printf \"%10.10s\" .CreatedSince}} {{printf \"%10s\" .Size}} {{printf \"%8s\" .Tag}} {{.ID}} {{printf .Repository}}"'

#
# $ d.images
#    4 days     129 MB    16.04 104bec311bcd ubuntu
#    8 days   1.398 GB   latest 54a3f229b1e8 platform_inspector
#    8 days   1.216 GB   <none> 596f60472eee <none>
#   2 weeks   705.9 MB   latest 11b8ffa38b53 952504897854.dkr.ecr.us-east-1.amazonaws.com/sftpingestor_ingestor
#   2 weeks   203.6 MB   latest 74f952112e81 952504897854.dkr.ecr.us-east-1.amazonaws.com/sftpingestor_sftp
#   4 weeks   672.1 MB      2.7 95dfb9bfd665 python
#   6 weeks     123 MB   jessie 73e72bf822ca debian
#  10 weeks   1.093 MB   latest e02e811dd08f busybox
#

alias d.ps='docker ps --format "{{printf \"%-15.15s\" .Image}} {{printf \"%30.30s\" .Names}}: {{printf \"%20.20s\" .Command}} || {{.Status}}"'

#
#  $ d.ps -a
# f11b6656088f                  high_stonebraker: "/bin/sh -c 'cd /com || Exited (1) 25 minutes ago
# 86272851efa1                     big_heyrovsky: "/bin/sh -c 'apt-get || Exited (100) 29 minutes ago
# platform_db                      platform_db_1: "/docker-entrypoint. || Up 9 seconds
#

alias d.ips='docker inspect --format "{{printf \"%30.30s\" .Name}} : {{printf \"%20.20s\" .NetworkSettings.IPAddress}}" $(docker ps -aq)'

#
# $ d.ips
#             /high_stonebraker :
#                /big_heyrovsky :
#                /platform_db_1 :           172.17.0.2
#            /sftpingestor_db_1 :
#
