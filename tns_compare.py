import requests
import urllib.request
import fruitbat
import math
from frbcat import TNS
from csv import reader
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz, Angle
import astropy.units as u
import numpy as np
import re
from googleapiclient import discovery
from google.oauth2 import service_account
import time

print('Running gitpull.php...')
start = time.time()
x = requests.get('http://www.herta-experiment.org/gitpull.php?plot=0', timeout=600) # 10 min timeout
print(x.content)
print(time.time() - start)
print('Done')

### Download TNS HTML and compare with FRBSTATS count to check if DB is up to date
# TNS
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
response = requests.get("https://www.wis-tns.org/search?&discovered_period_value=&discovered_period_units=days&unclassified_at=0&classified_sne=0&include_frb=1&name=frb&name_like=0&isTNS_AT=all&public=all&ra=&decl=&radius=&coords_unit=arcsec&reporting_groupid%5B%5D=null&groupid%5B%5D=null&classifier_groupid%5B%5D=null&objtype%5B%5D=null&at_type%5B%5D=5&date_start%5Bdate%5D=&date_end%5Bdate%5D=&discovery_mag_min=&discovery_mag_max=&internal_name=&discoverer=&classifier=&spectra_count=&redshift_min=&redshift_max=&hostname=&ext_catid=&ra_range_min=&ra_range_max=&decl_range_min=&decl_range_max=&discovery_instrument%5B%5D=null&classification_instrument%5B%5D=null&associated_groups%5B%5D=null&official_discovery=0&official_classification=0&at_rep_remarks=&class_rep_remarks=&frb_repeat=all&frb_repeater_of_objid=&frb_measured_redshift=0&frb_dm_range_min=&frb_dm_range_max=&frb_rm_range_min=&frb_rm_range_max=&frb_snr_range_min=&frb_snr_range_max=&frb_flux_range_min=&frb_flux_range_max=&num_page=500&display%5Bredshift%5D=0&display%5Bhostname%5D=0&display%5Bhost_redshift%5D=0&display%5Bsource_group_name%5D=0&display%5Bclassifying_source_group_name%5D=0&display%5Bdiscovering_instrument_name%5D=0&display%5Bclassifing_instrument_name%5D=0&display%5Bprograms_name%5D=0&display%5Binternal_name%5D=0&display%5BisTNS_AT%5D=0&display%5Bpublic%5D=0&display%5Bend_pop_period%5D=0&display%5Bspectra_count%5D=0&display%5Bdiscoverymag%5D=1&display%5Bdiscmagfilter%5D=0&display%5Bdiscoverydate%5D=1&display%5Bdiscoverer%5D=0&display%5Bremarks%5D=0&display%5Bsources%5D=0&display%5Bbibcode%5D=0&display%5Bext_catalogs%5D=0&display%5Brepeater_of_objid%5D=0&display%5Bdm%5D=1&display%5Bgalactic_max_dm%5D=0&display%5Bbarycentric_event_time%5D=0&display%5Bpublic_webpage%5D=0", headers=headers)

html = str(response.content)
print('++++++++++++++++++++++++++++++++++++++')
print(html)
print('++++++++++++++++++++++++++++++++++++++')
tns_count = str(html.split('out of <em class="placeholder">')[1][0:3])

# FRBSTATS
req = requests.get('https://www.herta-experiment.org/frbstats/catalogue.csv')
url_content = req.content
csv_file = open('catalogue_count.csv', 'wb')

csv_file.write(url_content)
csv_file.close()

frbstats_count = -3
with open('catalogue_count.csv', 'rt') as fin:
	for line in fin:
		frbstats_count += 1
		#frbstats_count = str(len(fin))

print('TNS: '+str(tns_count)+'\nFRBSTATS: '+str(frbstats_count))
success = True
if str(tns_count) <= str(frbstats_count):
	print('[+] The FRBSTATS database is up to date!')
else:
	success = False

# Read TNS catalogue
tns = TNS(path='/home/runner/', tns_name='user1', tns_id='id1')
df = tns.df
units = tns.units
print(df.to_string())
# Print entire dataframe for debugging in case TNS index changes again
#print(df.to_string())

tns_frbs = df.values[:,20]
print('__--__-_--_-_-_-_')
print(tns_frbs)
print('__-_----_-_-__')
# Read FRBSTATS CSV catalogue
blacklist = ['FRB 20180908B']
frbstats_frbs = []
for blacklisted_frb in blacklist:
	frbstats_frbs.append(blacklisted_frb)

with open('catalogue_count.csv', 'r') as read_obj:
	csv_reader = reader(read_obj)
	header = next(csv_reader)
	# Skip header
	if header != None:
		for row in csv_reader:
			frbstats_frbs.append(row[0])
print(frbstats_frbs)
frbstats_frbs = np.array(frbstats_frbs)
#print(tns_frbs)
#print(frbstats_frbs)
diff = np.in1d(tns_frbs, frbstats_frbs)


telescope_dict = {
	'Arecibo': 'Arecibo',
	'ATA': 'ATA',
	'ASKAP': 'ASKAP',
	'CRAFT': 'ASKAP',
	'SKA': 'SKA',
	'Tianlai': 'Tianlai',
	'CHIME': 'CHIME',
	'DSA': 'DSA',
	'Effelsberg': 'Effelsberg',
	'Meer': 'MeerKAT',
	'FAST': 'FAST',
	'GMRT': 'GMRT',
	'LPA_LPA': 'LPA',
	'LPA': 'LPA',
	'GBT': 'GBT',
	'GMRT': 'GMRT',
	'SRT_LP': 'INAF SRT',
	'Parkes': 'Parkes',
	'Pushchino LPA': 'Pushchino LPA',
	'Stockert': 'Stockert',
	'UTMOST': 'UTMOST',
	'MOST': 'UTMOST',
	'VLA': 'VLA',
	'WSRT': 'WSRT/Apertif',
	'Apertif': 'WSRT/Apertif',
	'Other': 'Other'
}

SERVICE_ACCOUNT_FILE = "gsheets.json"
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = discovery.build('sheets', 'v4', credentials=credentials)
spreadsheet_id = '1W27KNa6yJzYA_b8HLSz4hxtWEZQtxUhGTXfQjlXgpzY'
range_ = 'Catalogue!A1:P1'
value_input_option = 'USER_ENTERED'
insert_data_option = 'INSERT_ROWS'
print(diff)
count = 0
for i, element in enumerate(diff):
	if element == False:
		#print(frbstats_frbs[i])
		print(tns_frbs[i])
		print(x)
		frb_tns_url = 'https://www.wis-tns.org/object/'+([x.strip() for x in str(tns_frbs[i]).split('FRB')][1]).lower()

		print(frb_tns_url)
		response = requests.get(frb_tns_url, headers=headers)
		html = str(response.content)

		#try:
		utc = re.search(r'<td class=\"cell-discovery_date\">(.*?)</td><td class=\"cell-flux\">', html).group(1)
		mjd = str(Time(utc, format='iso', scale='utc').mjd)
		#except (AttributeError,ValueError,IndexError):
		#    utc = '-'
		#    mjd = '-'
		try:
			telescope = re.search(r'<td class=\"cell-tel_inst\">(.*?)</td><td class=\"cell-snr\">', html).group(1)
			for key, value in telescope_dict.items() :
				if telescope.lower() in key.lower():
					telescope = value
			if str(telescope) == '0' or str(telescope) == '0.0':
				telescope = '-'
		except (AttributeError,ValueError,IndexError):
			telescope = '-'
		try:
			ra = re.search(r'<td class=\"cell-ra\">(.*?)</td><td class=\"cell-decl\">', html).group(1).split()[0] #[1] to get the error
			if str(ra) == '0' or str(ra) == '0.0':
				ra = '-'
		except (AttributeError,ValueError,IndexError):
			ra = '-'
		try:
			if '(' in re.search(r'<td class=\"cell-ra\">(.*?)</td><td class=\"cell-decl\">', html).group(1) and ')' in re.search(r'<td class=\"cell-ra\">(.*?)</td><td class=\"cell-decl\">', html).group(1):
				ra_error = re.search(r'<td class=\"cell-ra\">(.*?)</td><td class=\"cell-decl\">', html).group(1).split()[1]
				ra_error = ra_error + re.search(r'<td class=\"cell-ra\">(.*?)</td><td class=\"cell-decl\">', html).group(1).split()[2]
				ra_error = ra_error.replace('(','').replace(')','')
				ra_error = str(round(Angle(ra_error).arcmin, 2))
				if ra_error == '0' or ra_error == '0.0':
					ra_error = '-'
			else:
				ra_error = '-'
		except (AttributeError,ValueError,IndexError):
			ra_error = '-'
		try:
			dec = re.search(r'<td class=\"cell-decl\">(.*?)</td><td class=\"cell-discovery_date\">', html).group(1).split()[0] #[1] to get the error
			if str(dec) == '0' or str(dec) == '0.0':
				dec = '-'
		except (AttributeError,ValueError,IndexError):
			dec = '-'
		try:
			if '(' in re.search(r'<td class=\"cell-decl\">(.*?)</td><td class=\"cell-discovery_date\">', html).group(1) and ')' in re.search(r'<td class=\"cell-decl\">(.*?)</td><td class=\"cell-discovery_date\">', html).group(1):				
				dec_error = re.search(r'<td class=\"cell-decl\">(.*?)</td><td class=\"cell-discovery_date\">', html).group(1).split()[1]
				dec_error = dec_error + re.search(r'<td class=\"cell-decl\">(.*?)</td><td class=\"cell-discovery_date\">', html).group(1).split()[2]
				dec_error = dec_error.replace('(','').replace(')','')
				dec_error = str(round(Angle(dec_error).arcmin, 2))
				if dec_error == '0' or dec_error == '0.0':
					dec_error = '-'
			else:
				dec_error = '-'
		except (AttributeError,ValueError,IndexError):
			dec_error = '-'
		if ra != '-' and dec != '-':
			equatorial = SkyCoord(ra=ra, dec=dec, unit=(u.hourangle, u.deg))
			galactic = equatorial.galactic
			l = str(round(galactic.l.deg, 2))
			b = str(round(galactic.b.deg, 2))
		try:
			frequency = re.search(r'<td class=\"cell-ref_freq\">(.*?)</td><td class=\"cell-inst_bandwidth\">', html).group(1).split()[0]
			if str(frequency) == '0' or str(frequency) == '0.0':
				frequency = '-'
		except (AttributeError,ValueError,IndexError):
			frequency = '-'
		try:
			dm = re.search(r'<td class=\"cell-dm\">(.*?)</td><td class=\"cell-galactic_max_dm\">', html).group(1).split()[0] #[1] to get error
			if str(dm) == '0' or str(dm) == '0.0':
				dm = '-'
		except (AttributeError,ValueError,IndexError):
			dm = '-'
		try:
			if '(' in re.search(r'<td class=\"cell-dm\">(.*?)</td><td class=\"cell-galactic_max_dm\">', html).group(1) and ')' in re.search(r'<td class=\"cell-dm\">(.*?)</td><td class=\"cell-galactic_max_dm\">', html).group(1):
				dm_error = re.search(r'<td class=\"cell-dm\">(.*?)</td><td class=\"cell-galactic_max_dm\">', html).group(1).split()[1].replace('(','').replace(')','')
				dm_error = str(dm_error)
				if dm_error == '0' or dm_error == '0.0':
					dm_error = '-'
			else:
				dm_error = '-'
		except (AttributeError,ValueError,IndexError):
			dm_error = '-'
		try:
			flux = re.search(r'<td class=\"cell-flux\">(.*?)</td><td class=\"cell-unit_name\">', html).group(1).split()[0] #[1] to get error
			if str(flux) == '0' or str(flux) == '0.0':
				flux = '-'
		except (AttributeError,ValueError,IndexError):
			flux = '-'
		try:
			width = re.search(r'<td class=\"cell-burst_width\">(.*?)</td><td class=\"cell-scattering_time\">', html).group(1).split()[0] #[1] to get error
			if str(width) == '0' or str(width) == '0.0':
				width = '-'
		except (AttributeError,ValueError,IndexError):
			width = '-'
		try:
			fluence = re.search(r'<td class=\"cell-fluence\">(.*?)</td><td class=\"cell-burst_width\">', html).group(1).split()[0] #[1] to get error
			if str(fluence) == '0' or str(fluence) == '0.0':
				fluence = '-'
		except (AttributeError,ValueError,IndexError):
			fluence = '-'
		try:
			snr = re.search(r'<td class=\"cell-snr\">(.*?)</td><td class=\"cell-fluence\">', html).group(1)
			if str(snr) == '0' or str(snr) == '0.0':
				snr = '-'
		except (AttributeError,ValueError,IndexError):
			snr = '-'

		reference = frb_tns_url
		if "Host Redshift" in html:
			try:
				redshift_measured = re.search(r'<span class=\"name\">Host Redshift</span><div class=\"value\"><b>(.*?)</b></div></div><div class=\"field field', html).group(1)
				if str(redshift_measured) == '0' or str(redshift_measured) == '0.0':
					redshift_measured = '-'
			except (AttributeError,ValueError,IndexError):
				redshift_measured = '-'
		else:
			redshift_measured = '-'
		redshift = '-'
		
		frb = fruitbat.Frb(float(dm), gl=l, gb=b)
		frb.calc_dm_galaxy()
		try: 
			# Calculate the Redshift of the FRB
			redshift = float(frb.calc_redshift())
			# Round to 4 decimal places
			redshift = round(redshift, 4)
			if math.isnan(redshift):
				print('is nan entered. Redshift is:')
				print(str(redshift))
				redshift = '-'
			else:
				redshift = str(redshift)
		except Exception as e:
			print(e)
			redshift = '-'
		
		print(utc, mjd, telescope, str(ra), str(dec), l, b, frequency, dm, flux, width, fluence, snr, reference, redshift, redshift_measured, ra_error, dec_error, dm_error)
		data = [[tns_frbs[i], utc, mjd, telescope, str(ra), '="'+str(dec)+'"', l, b, frequency, dm, flux, width, fluence, snr, reference, redshift, redshift_measured, ra_error, dec_error, dm_error]]
		res = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=range_, valueInputOption=value_input_option, insertDataOption=insert_data_option, body={"values": data}).execute()
		print(res)
		print('---')
		count += 1
		time.sleep(5)
		if count > 4:
			count = 0
			time.sleep(30)

print('Sorting...')
req = {
	"requests": [
		{
			"sortRange": {
				"range": {
					"sheetId": 1560822367,
					"startRowIndex": 1,
					"startColumnIndex": 0
				},
				"sortSpecs": [
					{
						"dataSourceColumnReference": {
							"name": "A"
						},
						"sortOrder": "ASCENDING"
					}
				]
			}
		}
	]
}
res = service.spreadsheets().batchUpdate(body=req, spreadsheetId=spreadsheet_id).execute()
print(res)

print('Running gitpull.php...')
start = time.time()
x = requests.get('http://www.herta-experiment.org/gitpull.php?plot=0', timeout=600) # 10 min timeout
print(x.status_code)
print(x.content)
print(time.time() - start)
print('Done')
if not success:
	raise ValueError('[-] The FRBSTATS database is out of date/has been modified!')
