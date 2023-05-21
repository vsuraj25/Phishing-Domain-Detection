from prediction_service.feature_extractor import FeatureExtractor
import joblib

invalid_url_msg = 'Seem like the URL you provided, is not qualified as a valid url. Please check the URL again!'
phish_url_msg = 'This URL is most likely phishing! It matches the qualities of a phishing URL!'
susp_url_msg = "This URL seems to be suspicious! Explore more about the URL before commiting anything!"
leg_url_msg = 'This URL is Legal. You can visit the URL freely!'
img_link = '../static/images/phshing1.webp'

model_path = 'artifacts/model_training/saved_models/model.joblib'
model = joblib.load(model_path)


def get_response(url):
    result = {
        'message' : None,
        'general_analysis_report' : None,
        'gif_link': None,
        'phis_prob' : None,
        'legal_prob': None
    }

    features = FeatureExtractor(url).get_feature_list()
    phish_prob = model.predict_proba(features)[0,0]
    legal_prob = model.predict_proba(features)[0,1]

    general_analysis =  FeatureExtractor(url).general_url_analysis()
    for val in general_analysis.values():
        if val != 0:
            result['message'] = invalid_url_msg
            result['general_analysis_report'] = general_analysis
            result['gif_link'] = img_link
            result['phis_prob'] = 'Invalid URL'
            result['legal_prob'] = 'Invalid URL'
            return result

    if phish_prob < 0.6 :
        result['message'] = leg_url_msg
    elif phish_prob > 0.6 and phish_prob < 0.8 :
        result['message'] = susp_url_msg
    else:
        result['message'] = phish_url_msg

    result['general_analysis_report'] = general_analysis
    result['gif_link'] = img_link
    result['phis_prob'] = phish_prob
    result['legal_prob'] = legal_prob
    return result





