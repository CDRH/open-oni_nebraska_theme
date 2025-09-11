# Nebraska Newspapers Batch Management

## One Time Setup Actions

These are steps that only need to be run once on a new Nebraska Newspapers server

Install cifs software to enable mounting network file shares

```bash
sudo yum install cifs-utils
```

Install bagit.py globally (separate from Open ONI virtual environment)

```bash
# Add to system-wide package list regularly updated
echo "bagit" | sudo tee -a /root/requirements.txt

# Manually install now
sudo pip install bagit
```

## nohup Utility
Several commands run throughout this process will take from around 45 minutes up
to many hours to complete. If one's terminal or SSH connection is closed, the
process will normally be interrupted and require some cleanup and restarting the
command again. To avoid this we can prefix these long-running commands with the
`nohup` utility and start them running in the background of the Bash shell by
appending an `&` at the end of the command.

This is most useful for `load_batch` which loads a batch's data into
Open ONI as this command usually takes multiple hours to complete and it's not
necessary to stay connected while this runs. For this, we take the normal
command

```bash
./manage.py load_batch /var/local/newspapers/batch_nbu_(batch_name_ver##) > (batch_name).txt
```

and modify as follows

```bash
nohup ./manage.py load_batch /var/local/newspapers/batch_nbu_(batch_name_ver##) > (batch_name).txt &
```

We can also chain commands together by putting them in a bash script file
and running it as `nohup load_multiple_batches.sh &`.

## Log Files
The use of `> (batch_name).txt` at the end ("redirection" in command line lingo)
saves the output from the command normally printed to one's terminal in a text
file. This can be done regardless of whether `nohup` is used, but without this
the `nohup` utility will save the output in `nohup.out`. We prefer to use a file
name that describes what action the text file is recording. This is often an
abbreviated form of the batch name. For example we can use `manyissues`
rather than the entire name `batch_nbu_manyissues_ver01`.

We assume the default action of these files is a load_batch command, but
one may also wish to use `nohup` with `rsync`, `bagit.py`, or `purge_batch`
commands which also run longer in case one expects to interrupt their network
connection by disconnect from the VPN or sleep / shutdown of their computer.
For these other actions, please prepend the log file name with the action.
For example a `purge_batch` log file could be named `purge_manyissues.txt`.

If having to repeat an action during troubleshooting, one might also wish to
date or number the log file so past action log files aren't overwritten,
e.g. `purge_manyissues-20230615.txt` or `purge_manyissues-2.txt`. After logs
are reviewed and any questions answered, please move them to a `log/` directory
adjacent to where they were created:

```bash
mv *.txt log/
```

## Transfer Batch Files to Dev Server

SSH into the server

```bash
ssh (active-directory-name@unl.edu)@nebnewspapers-dev.unl.edu
# Example: ssh lweakly2@unl.edu@nebnewspapers-dev.unl.edu
```

Mount the network share from libr1901 to transfer files to the server

```bash
# Make directory to use as mount point
cd [~]
# Only one time and can skip for future ingests
mkdir libr1901-newspapers

sudo mount -t cifs -o username=(active-directory-name but no "@unl.edu") \
  //libr1901.unl.edu/newspapers/ libr1901-newspapers/
# Example:
# sudo mount -t cifs -o username=gtunink2 //libr1901.unl.edu/newspapers/ libr1901-newspapers/

# This will prompt you for your Active Directory password twice:
# once for sudo, and once for connecting to libr1901

# Batches on libr1901 should have a directory structure like:
libr1901-newspapers/batch_nbu_(batch name)/
├─── (lccn)
│    └── (reel)
├─── ...
├─── batch.xml
└─── batch_1.xml

# View tree of top directories and files to confirm expected structure
tree -L 2 libr1901-newspapers/batch_nbu_(batch name)/

# This rsync command is resumable if interrupted and usually takes up to 45 min.
# The % progress and time estimates shown are often optimistically inaccurate.
# Explanation of rsync options: https://explainshell.com/explain?cmd=rsync+-ahuX+--del
# Note that omission and presence of trailing slashes here matters,
# so type carefully and double-check before submitting the command!
rsync -ahuX --del --info=progress2 --exclude=""*.tif"" libr1901-newspapers/batch_nbu_(batch_name) /var/local/newspapers/
# Example:
# rsync -ahuX --del --info=progress2 --exclude=""*.tif"" libr1901-newspapers/batch_nbu_manyissues /var/local/newspapers/
```

### Record Batch Storage Info
Record under the Size columns on the [Newspaper Batch Information
spreadsheet](https://uofnelincoln.sharepoint.com/:x:/r/sites/UNL-UniversityLibraries/DISC/cdrh/Shared%20Documents/CDRH%20Projects/Project%20Folders/Newspapers/Newspapers_General/Newspaper%20Batch%20Information.xlsx?d=w0f0beecd41ca47d48c581b4618d37c77&csf=1&web=1&e=bcK4Hb)

```bash
# Size including tiffs on libr1901
du -sh libr1901-newspapers/batch_nbu_(batch_name)

# Size without tiffs (because the batch was rsynced over without them)
du -sh /var/local/newspapers/batch_nbu_(batch_name)
```

### Unmount Network Share
Unmount after transfers complete. The `libr1901-newspapers` directory will
appear empty after successful unmount.

```bash
sudo umount libr1901-newspapers

ls libr1901-newspapers
# No output here indicates an empty directory and successful unmount
```

### Prepare Files for Ingest
Set an ONI-compatible directory name, permissions, and add a README file.

```bash
cd /var/local/newspapers

# Set ONI-compatible directory name
# Typically end with ver01 unless LoC corrections were made
# Note in "ver" column of Newspaper Batch Information spreadsheet if not "ver01"
mv batch_nbu_(batch_name) batch_nbu_(batch_name_ver##)
# Example: mv batch_nbu_manyissues batch_nbu_manyissues_ver01


# Set group-writeable, global-readable batch permissions
# These commands may run for 10-15 minutes on the long end. Unfortunately there
# is no way to know its progress, so please be patient.
chmod -R g+rwX batch_nbu_(batch_name_ver##)
chmod -R o+rX batch_nbu_(batch_name_ver##)

# Check permissions include group write permissions now
tree -pL 2 batch_nbu_(batch_name_ver##)

batch_nbu_(batch_name_ver##)/
├── [-rwxrwxr-x]  batch_1.xml
├── [-rwxrwxr-x]  batch.xml
└── [drwxrwxr-x]  (lccn))
    └── [drwxrwxr-x]  (reel)
```

Create README.txt file with fields noted in example

`nano batch_nbu_(batch_name_ver##)/README.txt`:

```
batch_name: nbu_(batch_name)
canonical: libr1901
contents: (List the titles and their LCCNs here as
  "Title (lccn)[, Title (lccn), ...]"
  Before ingest, the LCCNs are the top level directories
  but one has to look at the XML files to find the title text
  in batch_nbu_(batch_name_ver##)/(lccn)/(reel #)/(reel #).xml and search
  for the "<ndnp:titles>" element.)
loc: ("yes" if NDNP batch, "no" otherwise)
description: (Most batches have nothing to note here. This is for unusual
  circumstances, e.g. to articulate what LCCN changes were made, alterations
  to dates, etc needed to recreate batch if copied from canonical location
  again, or any other problems)
```

Example from `batch_nbu_keithsbear_ver03`:
```
batch_name: nbu_keithsbear_ver03
canonical: libr1901
contents: The Frontier (2010270509), The Monitor (sn94055234), Omaha Monitor (sn94055235)
loc: yes
description: Corrected version received from LoC
```

### Create Checksums and Manifests
There should be no more editing of files after creating checksums and manifests
unless ingest errors are being corrected. This step moves files into a `data/`
directory and SHOULD NOT BE RERUN without moving them back out before new
checksums and manifests are created.

```bash
bagit.py --quiet --md5 batch_nbu_(batch_name_ver##)
```

The batch directory should look like this afterwards:

```
batch_nbu_(batch_name_ver##)/
├── bag-info.txt
├── bagit.txt
├── data
│   ├── batch_1.xml
│   ├── batch.xml
│   ├── README.txt
│   └── (lccn))
├── manifest-md5.txt
└── tagmanifest-md5.txt
```

```bash
tree -L 2 batch_nbu_(batch_name_ver##)
```

#### Reset Files to Recreate Checksums and Manifests
**Only if** the checksums and manifest creation is **interrupted** or **errors
need corrected after a failed ingest**, we must delete them and move files out
of the `data/` directory

```bash
cd /var/local/newspapers/batch_nbu_(batch_name_ver##)

# Delete all files in this directory but not (sub)directories
rm *.*

# Move all files in the data/ directory to the current directory; remove data/
mv data/* .
rmdir data

# Return to parent directory
cd ..
```

Return to [Create Checksums and Manifests](#create-checksums-and-manifests) above
to recreate

## Dev Server Ingest

```bash
cd /var/local/www/django/openoni

# Load the Open ONI Python virtual environment
. ENV/bin/activate

# It's not necessary for our use, but one my unload the virtual environment
# by later running the command `deactivate`

# This command usually takes many hours to complete so we use nohup and run the
# command in the background so we can disconnect SSH and it will still run
nohup ./manage.py load_batch /var/local/newspapers/batch_nbu_(batch_name_ver##) > (batch_name).txt &
# Example:
# nohup ./manage.py load_batch /var/local/newspapers/batch_nbu_manyissues_ver01 > manyissues.txt &

# One can print the end of the log file to ensure the command is progressing
tail (batch_name).txt

# Or follow log info as it is recorded, but note this does slow down the
# ingest process a little. Press Ctrl + C to quit following what's written.
tail -f (batch_name).txt

# After completion, review the log for errors etc, move to log directory
nano (batch_name).txt
mv (batch_name).txt log/
```

If an error occurred during batch ingest, ask a developer for help parsing the
log file. We will likely need to edit files to fix errors and then follow steps
in [Reset Files to Recreate Checksums and
Manifests](#reset-files-to-recreate-checksums-and-manifests).

After batch ingest completes, compare the batch info in Open ONI and Chronicling
America if an NDNP batch:
- https://nebnewspapers-dev.unl.edu/batches
- https://nebnewspapers.unl.edu/batches
- https://chroniclingamerica.loc.gov/awardees/nbu/

Record the issue and page counts in the [Newspaper Batch Information
spreadsheet](https://uofnelincoln.sharepoint.com/:x:/r/sites/UNL-UniversityLibraries/DISC/cdrh/Shared%20Documents/CDRH%20Projects/Project%20Folders/Newspapers/Newspapers_General/Newspaper%20Batch%20Information.xlsx?d=w0f0beecd41ca47d48c581b4618d37c77&csf=1&web=1&e=bcK4Hb)

### Word Coordinates Files Permissions
Directories and files created during ingest process have permissions
which cause errors if additional or reworked issues/pages are ingested
in the same LCCN by a different user. We run this command to set permissions
which avoid these errors. It might have to be run with `sudo` by a developer if
this step is missed before a subsequent ingest.

```bash
# This command can take 15-20 minutes to complete
chmod -R g+rwX /var/local/www/django/openoni/data/word_coordinates/lccn/ 2>/dev/null
```

## Production Server Transfer and Ingest

SSH into the server

```bash
ssh (active-directory-name@unl.edu)@nebnewspapers.unl.edu
# Example: ssh lweakly2@unl.edu@nebnewspapers.unl.edu

cd /var/local/newspapers/

# Transfer batch from dev server (~45min)
rsync -ahuX --del --info=progress2 nebnewspapers-dev.unl.edu:/var/local/newspapers/batch_nbu_(batch_name_ver##) .
# Example:
# rsync -ahuX --del --info=progress2 nebnewspapers-dev.unl.edu:/var/local/newspapers/batch_nbu_manyissues_ver01 .

# Validate batch checksums and manifest
# Initial fast validation; if validation errors occur, notify a developer
bagit.py --validate --fast batch_nbu_(batch_name_ver##)

# Thorough validation after fast one succeeds
# May omit --quiet if you prefer to see every file printed as it is processed
# rather than only see errors, but this does slow the process down
bagit.py --validate --quiet batch_nbu_(batch_name_ver##)

cd /var/local/www/django/openoni

# Load the Open ONI Python virtual environment
. ENV/bin/activate

# This command usually takes many hours to complete so we use nohup and run the
# command in the background so we can disconnect SSH and it will still run
nohup ./manage.py load_batch /var/local/newspapers/batch_nbu_(batch_name_ver##) > (batch_name).txt &
# Example: nohup ./manage.py load_batch /var/local/newspapers/batch_nbu_manyissues_ver01 > manyissues.txt &

# One can print the end of the log file to ensure the command is progressing
tail (batch_name).txt

# Or follow log info as it is recorded, but note this does slow down the
# ingest process a little. Press Ctrl + C to quit following what's written.
tail -f (batch_name).txt

# After completion, review the log for errors etc, move to log directory
nano (batch_name).txt
mv (batch_name).txt log/
```

## Purge a Batch
Purging a batch is necessary if an error occurs or data needs correction

```bash
cd /var/local/www/django/openoni

# Load the Open ONI Python virtual environment
. ENV/bin/activate

./manage.py purge_batch (batch_name) > purge_(batch_name).txt
# Example: ./manage.py purge_batch batch_nbu_manyissues_ver01 > purge_manyissues.txt

# There is no progress output as the purge occurs, but we should review the log
# after the command completes
nano purge_(batch_name).txt
mv purge_(batch_name).txt log/
```

## Miscellaneous Tasks
Note these shouldn't be used without consulting a developer as they are risky
data modifying processes.

### Change LCCN by Directory
Be careful with this one as it changes files in place.
Suggest one copy the entire directory first before running,
then change the batch files to reflect new LCCN.

```bash
cd /var/local/newspapers/batch_nbu_(batch_name_ver##)/data/
find ./(LCCN-wrong) -type f -name ""*.xml"" -exec sed -i '' 's/(LCCN-wrong)/(LCCN-fix)/g' {} \+
```

### Copy Media Files Into Identical Directory Structure
`-n` to print out the files it will move without moving them (aka dry run).
Remove this after dry run to actually move the files.

Need to be very sure that the directory structure matches
and that to and from paths are starting from the same place!!!

```bash
rsync -ahuX --info=progress2 -n tiff/location/ new/location/ \
  --include="*/" \
  --include="*.jp2" \
  --include="*.pdf" \
  --exclude="*"
```
