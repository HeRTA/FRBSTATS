import requests
import urllib.request
from frbcat import TNS
from csv import reader
from astropy.time import Time
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
import astropy.units as u
import numpy as np
import re
from googleapiclient import discovery

### Download TNS HTML and compare with FRBSTATS count to check if DB is up to date
# TNS
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
response = requests.get("https://www.wis-tns.org/search?&discovered_period_value=&discovered_period_units=days&unclassified_at=0&classified_sne=0&include_frb=1&name=frb&name_like=0&isTNS_AT=all&public=all&ra=&decl=&radius=&coords_unit=arcsec&reporting_groupid%5B%5D=null&groupid%5B%5D=null&classifier_groupid%5B%5D=null&objtype%5B%5D=null&at_type%5B%5D=5&date_start%5Bdate%5D=&date_end%5Bdate%5D=&discovery_mag_min=&discovery_mag_max=&internal_name=&discoverer=&classifier=&spectra_count=&redshift_min=&redshift_max=&hostname=&ext_catid=&ra_range_min=&ra_range_max=&decl_range_min=&decl_range_max=&discovery_instrument%5B%5D=null&classification_instrument%5B%5D=null&associated_groups%5B%5D=null&official_discovery=0&official_classification=0&at_rep_remarks=&class_rep_remarks=&frb_repeat=all&frb_repeater_of_objid=&frb_measured_redshift=0&frb_dm_range_min=&frb_dm_range_max=&frb_rm_range_min=&frb_rm_range_max=&frb_snr_range_min=&frb_snr_range_max=&frb_flux_range_min=&frb_flux_range_max=&num_page=500&display%5Bredshift%5D=0&display%5Bhostname%5D=0&display%5Bhost_redshift%5D=0&display%5Bsource_group_name%5D=0&display%5Bclassifying_source_group_name%5D=0&display%5Bdiscovering_instrument_name%5D=0&display%5Bclassifing_instrument_name%5D=0&display%5Bprograms_name%5D=0&display%5Binternal_name%5D=0&display%5BisTNS_AT%5D=0&display%5Bpublic%5D=0&display%5Bend_pop_period%5D=0&display%5Bspectra_count%5D=0&display%5Bdiscoverymag%5D=1&display%5Bdiscmagfilter%5D=0&display%5Bdiscoverydate%5D=1&display%5Bdiscoverer%5D=0&display%5Bremarks%5D=0&display%5Bsources%5D=0&display%5Bbibcode%5D=0&display%5Bext_catalogs%5D=0&display%5Brepeater_of_objid%5D=0&display%5Bdm%5D=1&display%5Bgalactic_max_dm%5D=0&display%5Bbarycentric_event_time%5D=0&display%5Bpublic_webpage%5D=0", headers=headers)

html = str(response.content)

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
if str(tns_count) == str(frbstats_count):
	print('[+] The FRBSTATS database is up to date!')
else:
	success = False

# Read TNS catalogue
tns = TNS(path='/home/runner/', tns_name='my_user_name', tns_id='my_user_id')
df = tns.df
units = tns.units

# Print entire dataframe for debugging in case TNS index changes again
#print(df.to_string())

tns_frbs = df.values[:,27]

# Read FRBSTATS CSV catalogue
frbstats_frbs = []
with open('catalogue_count.csv', 'r') as read_obj:
	csv_reader = reader(read_obj)
	header = next(csv_reader)
	# Skip header
	if header != None:
		for row in csv_reader:
			frbstats_frbs.append(row[0])

frbstats_frbs = np.array(frbstats_frbs)
#print(tns_frbs)
#print(frbstats_frbs)
diff = np.in1d(tns_frbs, frbstats_frbs)

"""
telescopes = {
	'Arecibo': 'Arecibo',
	'ATA': 'ATA',
	'CRAFT': 'ASKAP',
	'CRAFT': 'ASKAP',
	'Tianlai': 'Tianlai',
	'CHIME': 'CHIME',
	'DSA-10': 'DSA-10',
	'Effelsberg': 'Effelsberg',
	'FAST': 'FAST',
	'GBT': 'GBT',
	'GMRT': 'GMRT',
	'INAF SRT': 'INAF SRT',
	'Parkes': 'Parkes',
	'Pushchino LPA': 'Pushchino LPA',
	'Stockert': 'Stockert',
	'UTMOST': 'UTMOST',
        'VLA': 'VLA',
        'WSRT/Apertif': 'WSRT/Apertif'
}
"""
for i, element in enumerate(diff):
	if element == False:
		#print(frbstats_frbs[i])
		print(tns_frbs[i])
		frb_tns_url = 'https://www.wis-tns.org/object/'+([x.strip() for x in str(tns_frbs[i]).split('FRB')][1]).lower()

		print(frb_tns_url)
		response = requests.get(frb_tns_url, headers=headers)
		html = str(response.content)

		#try:
		utc = re.search(r'<td class=\"cell-discovery_date\">(.*?)</td><td class=\"cell-flux\">', html).group(1)
		print(utc)
		mjd = Time(utc, format='iso', scale='utc').mjd
		#except (ValueError,IndexError):
		#    utc = '-'
		#    mjd = '-'
		try:
		    telescope = re.search(r'<td class=\"cell-tel_inst\">(.*?)</td><td class=\"cell-snr\">', html).group(1)
		except (ValueError,IndexError):
		    telescope = '-'
		try:
		    ra = re.search(r'<td class=\"cell-ra\">(.*?)</td><td class=\"cell-decl\">', html).group(1).split()[0] #[1] to get the error
		except (ValueError,IndexError):
		    ra = '-'
		try:
		    dec = re.search(r'<td class=\"cell-decl\">(.*?)</td><td class=\"cell-snr\">', html).group(1).split()[0] #[1] to get the error
		except (ValueError,IndexError):
		    dec = '-'
		if ra != '-' and dec != '-':
		    print(ra,dec)
		    equatorial = SkyCoord(ra=ra, dec=dec, unit=(u.hourangle, u.deg))
		    galactic = equatorial.galactic
		    l = str(round(galactic.l.deg, 2))
		    b = str(round(galactic.b.deg, 2))
		try:
		    frequency = re.search(r'<td class=\"cell-ref_freq\">(.*?)</td><td class=\"cell-inst_bandwidth\">', html).group(1).split()[0]
		except (ValueError,IndexError):
		    frequency = '-'
		try:
		    dm = re.search(r'<td class=\"cell-dm\">(.*?)</td><td class=\"cell-galactic_max_dm\">', html).group(1).split()[0] #[1] to get error
		except (ValueError,IndexError):
		    dm = '-'
		try:
		    flux = re.search(r'<td class=\"cell-flux\">(.*?)</td><td class=\"cell-unit_name\">', html).group(1).split()[0] #[1] to get error
		except (ValueError,IndexError):
		    flux = '-'
		try:
		    width = re.search(r'<td class=\"cell-burst_width\">(.*?)</td><td class=\"cell-scattering_time\">', html).group(1).split()[0] #[1] to get error
		except (ValueError,IndexError):
		    width = '-'
		try:
		    fluence = re.search(r'<td class=\"cell-fluence\">(.*?)</td><td class=\"cell-burst_width\">', html).group(1).split()[0] #[1] to get error
		except (ValueError,IndexError):
		    fluence = '-'
		try:
		    snr = re.search(r'<td class=\"cell-snr\">(.*?)</td><td class=\"cell-fluence\">', html).group(1)
		except (ValueError,IndexError):
		    snr = '-'

		reference = frb_tns_url
		redshift = '-'
		print(utc, mjd, telescope, ra, dec, l, b, frequency, dm, flux, width, fluence, snr, reference, redshift)
		print('---')
credentials = {
  "type": "service_account",
  "project_id": "bustling-art-337717",
  "private_key_id": "1617f62ed7d5a85846be361118927633a87e1705",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDBuG35GgxPNFVh\n8LwS1W2AQU4qGR7Zgcirx2hv67vLgGTopTwt5AJPckgGPt3CBWRHrq+MBvpUP3Or\nVrmZoAp2WWB8+q2rZTsWrgbGgX6U8brs8ZCGh3uPXJNvWNJXN/K6rPCh1rG8ZmBt\nmGtbDUJtJvHrWuiocpMrHLIKaiAqw3FlITuG4pOIGBy8ZdiaCZDAVk8WDyfnEQrT\nhO+HwnBvQYuevdZ9z1vxocvnoWQ5aj6lsWLjklWo0eWWvF6fGAZ9tE1eRAT0K9Jf\n2uxi+2kHed8ue4ZzvuvDqSN3M/pfOcZDYlzw/qyOUcpdkE8ddrN/4UzKSY8bBn4l\nCVvXsO7xAgMBAAECggEAAPMn4YzLJVLwXZE8mtWzumlCOi/yrXEBduDSFkUQSqh6\ngNmD41sMLS+LmDGUDMYnU7f7jF2MZKqwT9VrsOEkAVM23JCuFqUMa8lhUcqDawo0\nYcJddGC9rlpEhCCUshtyyToyg9igTngss4eHyePVa4uWrBIUtJ67Mf7rWzm3UVOv\nJCL3kdq43DhZQa+VjMx0HgVs5HjhTX22WM2CMclTjbrUzhsqnSLuDGCrWh367rq8\nesZFort6RhIijV+A6dGckySVmMac5hxxpICO2Ilzm/AJmjgVoq3ADZrq8L7YN+/g\nJndZjLznfm33crHzIoyjQMHhDGi65Ss2dTKjedfXAQKBgQDq4KaxO3uEfxDEkLhl\nAVQr3WWRTfG5MK1R4ue5t5McLUQa5FXBD7k7kZF8r3Eg53h6epDLDoykPq60TvfI\n/EB4bMpkIQ7vIxdpz1AQdfWyTvSh9f1/vuzT7HhpUKiu+IxiY+OMZZxatSs7x0g7\nGZOM+lfMT36BnIENO8p3yVkCyQKBgQDTJEJ5tNzt4uMdMFGlN4K9NJDxYco51fqw\nkBC7J6ubHhkp35uPWKyNRod+7MUz4iRSXgwVcEjf+1a+80Z7Fr03bGe6eqZ5Fy4Z\nNH+xoE3Ua0InPYWT6Ewy6QGNzgSvKP4NBzJSEWVSYQQhthjxoDfBj0H0kL7cLjxx\npXN3Ut826QKBgF2mk3BpajeLPpFRruQ/ImOXFE9ah74yZXkYAxMu2g5LEjOyxWqE\nLXRN93eCsJXRFV2ojyEXvQYkJB6queu+gKpDnnNMJxs8n7JFwgO+NOgSyUHmxlvw\nMZfSWrSLP6b8XWVBtNIfFbepMwLT074U1ZtJmkZRj/x3/ZDcPT+D3eTZAoGAA+Av\nhDJot8kpaBjB9uls8fIsEvI7lxIxdto+JGFXChLkXVtobJoxGKrJw++uswQcrJJj\nYGVeQRZJAlpO2eWR9Zl80fR8Z86gHwBSs70AkLyjSzsa35stAuY6DBNTDLAQ8cZH\nCzCcjoWPYNsJ3C2XuGrbyBR8HGiQ3XkvBGq2BDkCgYEA21MnTCWVw74Pckvg4TlI\neYiKcokQvBLA89C8PGXLo1sAHpuWL5vgh3/3cA+T9Hx/wbSA2oM4jlvuOaUv5BVt\nqvYM/ucUY9jvWk2ACoPAU10ReNPcIybGojaVP3qUXQYvKWvyNqKBdlOk6HNFrx83\nqp1qv8XtgeQvDOQl8PqNYIo=\n-----END PRIVATE KEY-----\n",
  "client_email": "frbstats@bustling-art-337717.iam.gserviceaccount.com",
  "client_id": "112685322460464860918",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/frbstats%40bustling-art-337717.iam.gserviceaccount.com"
}
service = discovery.build('sheets', 'v4', credentials=credentials)
spreadsheet_id = '1W27KNa6yJzYA_b8HLSz4hxtWEZQtxUhGTXfQjlXgpzY'
range_ = 'A813'
value_input_option = 'abc'
insert_data_option = value_input_option
request = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=range_, valueInputOption=value_input_option, insertDataOption=insert_data_option) #, body=value_range_body)
response = request.execute()
print(response)

if not success:
	raise ValueError('[-] The FRBSTATS database is out of date!')
