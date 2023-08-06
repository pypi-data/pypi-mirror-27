# Diff Disk Dump

## Overwiev
This program can create diff files of large files or block devices. I write it for creating VM disks diffs.

## Install
```
pip install diff-dd
```

## CLI Usage

Backup examples:
```
diff-dd --if /backup/full_disk_copy.raw --df /dev/lvm/changed_disk_snapshot --of /backup/diff_disk_copy.ddd
diff-dd --if /backup/full_disk_copy.raw --df /dev/lvm/changed_disk_snapshot > /backup/diff_disk_copy.ddd
diff-dd --if /backup/full_disk_copy.raw --df /dev/lvm/changed_disk_snapshot | gzip > /backup/diff_disk_copy.ddd.gz
diff-dd --if <(zcat /backup/full_disk_copy.raw.gz) --df /dev/lvm/changed_disk_snapshot --of /backup/diff_disk_copy.ddd
zcat /backup/full_disk_copy.raw.gz | ddd --df /dev/lvm/changed_disk_snapshot --of /backup/diff_disk_copy.ddd
cat /dev/lvm/changed_disk_snapshot | diff-dd --if <(zcat /backup/full_disk_copy.raw.gz) --of /backup/diff_disk_copy.ddd
diff-dd --if <(ssh remotehost cat /backup/full_disk_copy.raw) --df <(ssh remote2host cat /dev/lvm/changed_disk_snapshot) | ssh remote3host dd of=/backup/diff_disk_copy.ddd
```

Restore examples:
```
diff-dd --mode restore --if /backup/full_disk_copy.raw --df /backup/diff_disk_copy.ddd --of /dev/lvm/disk
diff-dd --mode restore --if <(zcat /backup/full_disk_copy.raw.gz) --df <(zcat /backup/diff_disk_copy.ddd.gz) > /dev/lvm/disk
zcat /backup/full_disk_copy.raw.gz | diff-dd --mode restore --df <(ssh remotehost cat /backup/diff_disk_copy.ddd.gz) | ssh remote2host dd of=/dev/lvm/disk
```

## API Usage
Backup:
```
from diff_dd import CreateDiff
iffd = open('/backup/full_disk_copy.raw', 'rb')
dffd = open('/dev/lvm/changed_disk_snapshot', 'rb')
offd = open('/backup/diff_disk_copy.ddd', 'wb')

differ = CreateDiff(iffd=iffd, dffd=dffd, offd=offd, block_size=16384)
differ.start()
```

Restore:
```
from diff_dd import ResoreDiff
iffd = open('/backup/full_disk_copy.raw', 'rb')
dffd = open('/backup/diff_disk_copy.ddd', 'rb')
offd = open('/dev/lvm/disk', 'wb')

differ_retore = ResoreDiff(iffd=iffd, dffd=dffd, offd=offd, block_size=16384)
differ_retore.start()
```
