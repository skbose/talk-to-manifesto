import os
from pathlib import Path

# define constants for the assistant and vector store
PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
ASSISTANT_NAME = "marathi_manifesto_interpreter"
VECTOR_STORE_NAME = "manifesto"
ASSISTANT_INSTRUCTIONS = (
    "तुम्हाला एका राजकारण्याचा वचननामा  दिला जातो. आता जनता तुम्हाला प्रश्न विचारेल "
    "आणि दिलेल्या वचननाम्याच्या आधारे तुम्हाला त्यांची उत्तरे द्यावी लागतील."
)
ASSISTANT_INSTRUCTIONS_2 = (
    "तुम्ही राजकारणी आहात. तुमच्याकडे तुमची वचननामा फाईल आहे."
    "लोक तुम्हाला प्रश्न विचारतील आणि तुम्हाला थोडक्यात आणि अचूक उत्तर द्यावे लागेल."
    "उत्तर हा तुमच्या जाहीरनाम्याचा भाग असावा. कृपया प्रथम व्यक्तीच्या भाषणात उत्तर द्या."
)
ASSISTANT_MODEL = "gpt-4o-mini"
TEXT_FILE_PATHS = [os.path.join(PROJECT_ROOT, "resources/manifesto.docx")]
RESPONSE_FORMAT = "Return an elaborate answer in marathi without any format."
