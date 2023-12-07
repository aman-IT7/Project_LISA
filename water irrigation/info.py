# Latitude: 34 deg; 54 min N
# Longitude: 86 deg; 36 min W


# Latitude: 34.9 degrees North
# Longitude: -86.6 degrees (West longitudes are represented as negative values)


lat, long = (34.6, -86.6)  # location of bragg farm


dataset_columns_preedit = """ Site Id	Date	Time	SMS.I-1:-2 (pct)  (loam)	SMS.I-1:-4 (pct)  (loam)	SMS.I-1:-8 (pct)  (loam)	SMS.I-1:-20 (pct)  (loam)	SMS.I-1:-40 (pct)  (loam)	STO.I-1:-2 (degC) 	STO.I-1:-4 (degC) 	STO.I-1:-8 (degC) 	STO.I-1:-20 (degC) 	STO.I-1:-40 (degC) 	tempmax	tempmin	temp	feelslikemax	feelslikemin	feelslike	dew	humidity	precip	precipprob	precipcover	preciptype	snow	snowdepth	windgust	windspeed	winddir	sealevelpressure	cloudcover	visibility	solarradiation	solarenergy	uvindex	severerisk	sunrise	sunset	moonphase	conditions	description	icon	stations """


def load_preproccess_scale_transform(csv_filepath):
    dataset = pd.read_csv(csv_filepath)
    dataset.drop(
        [
            "Date",
            "SM_2",
            "SM_8",
            "SM_20",
            "SM_40",
            "ST_2",
            "ST_8",
            "ST_20",
            "ST_40",
            "solarenergy",
            "precipprob",
            "preciptype",
            "snow",
            "snowdepth",
            "windgust",
            "winddir",
            "sealevelpressure",
            "visibility",
            "solarenergy",
            "uvindex",
            "severerisk",
            "icon",
            "stations",
            "dew",
            "solarradiation",
            "Time",
            # "cloudcover",
            "feelslike",
            # "windspeed",
        ],
        inplace=True,
        axis=1,
    )
    dataset.dropna(inplace=True)

    X = dataset.iloc[:, 1:].values
    y = dataset.iloc[:, 0].values

    ct = ColumnTransformer(
        transformers=[("encoder", OneHotEncoder(), [-1])], remainder="passthrough"
    )

    X = np.array(ct.fit_transform(X))
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, random_state=0
    )
    sc = MinMaxScaler()
    X_train[:, 9:] = sc.fit_transform(X_train[:, 9:])
    X_test[:, 9:] = sc.transform(X_test[:, 9:])

    X_train, y_train, X_test, y_test = map(
        np.asarray, [X_train, y_train, X_test, y_test]
    )
    X_train, X_test = map(lambda x: x.astype("float32"), [X_train, X_test])

    return (X_train, y_train), (X_test, y_test)
