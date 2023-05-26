from prediction_service.feature_extractor import FeatureExtractor
import joblib

invalid_url_msg = 'Unable to load the url! Seem like the URL you provided, either does not exist or not qualified as a valid url!'
phish_url_msg = 'This URL is most likely phishing! It matches the qualities of a phishing URL!'
susp_url_msg = "This URL seems to be suspicious! Explore more about the URL before commiting anything!"
leg_url_msg = 'This URL is Legal. You can visit the URL freely!'
invalid_link = '../static/images/404-not-found.webp'
verified_url = "../static/images/verified.webp"
suspicious_url = "../static/images/suspicious_url.webp"
phish_url = "../static/images/mi.webp"

model_path = 'artifacts/model_training/saved_models/model.joblib'
model = joblib.load(model_path)


def get_response(url):
    result = {
        'message' : None,
        'desc_message': None,
        'general_analysis_report' : None,
        'gif_link': None,
        'phis_prob' : None,
        'legal_prob': None
    }

    features = FeatureExtractor(url).get_feature_list()
    phish_prob = round(model.predict_proba(features)[0,0] * 100, 2)
    legal_prob = round(model.predict_proba(features)[0,1] * 100, 2)

    general_analysis =  FeatureExtractor(url).general_url_analysis()
    result_list = [res for res in list(general_analysis.values()) if res != 0]
    for val in general_analysis.values():
        if val != 0:
            result['message'] = invalid_url_msg
            result['desc_message'] = "Please provide a valid url!"
            result['general_analysis_report'] = result_list
            result['gif_link'] = invalid_link
            result['phis_prob'] = 'Invalid URL'
            result['legal_prob'] = 'Invalid URL'
            return result
        else:
            if len(result_list) > 0:
                general_analysis = result_list
            else:
                general_analysis = "Gereral Checks Passed Successfully!"
            

    if phish_prob < 55 :
        result['message'] = leg_url_msg
        result['gif_link'] = verified_url
        result['desc_message'] = f"The provided url passes all the validity checks with the legality percentage - {legal_prob}%"
    elif phish_prob > 50 and phish_prob < 80 :
        result['message'] = susp_url_msg
        result['gif_link'] = suspicious_url
        result['desc_message'] = f"The legality percentage of the provided url is {legal_prob}% making it suspicious! Please research more before commiting anything!"
    else:
        result['message'] = phish_url_msg
        result['gif_link'] = phish_url
        result['desc_message'] = f"According to our phishing detection system, this url fails all the validity checks! Please do not provide any valuable information or install any application at this website! "

    result['general_analysis_report'] = general_analysis
    result['phis_prob'] = phish_prob
    result['legal_prob'] = legal_prob
    return result





