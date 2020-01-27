
def CleanPetData(df):
	df = df.drop(['Unnamed: 0',
                      'url',
                      'type',
                      'species',
                      'tags',
                      'description',
                      'attributes.declawed',
                      'contact.address.address1',
                      'contact.address.address2',
                      'contact.address.state',
                      'contact.address.postcode',
                      'contact.address.country',
                      'photos',
                      'colors.primary',
                      'colors.secondary',
                      'colors.tertiary',
                      '_links.self.href',
                      '_links.type.href'], axis=1)
	return df 



def ReformatDates(df):
	fmt ='%Y-%m-%dT%H:%M:%S+0000'
	df['published_at'] =  pd.to_datetime(df['published_at'], format=fmt)
	df['status_changed_at'] =  pd.to_datetime(df['status_changed_at'], format=fmt)
	df['time_diff'] = df['status_changed_at'] - df['published_at']
	df['target_hour'] = df.time_diff.astype('timedelta64[h]')
	return df