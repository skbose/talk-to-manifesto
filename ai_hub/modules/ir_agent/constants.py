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
ASSISTANT_MODEL = "gpt-3.5-turbo"
TEXT_FILE_PATHS = [os.path.join(PROJECT_ROOT, "resources/manifesto.docx")]
RESPONSE_FORMAT = "Return an elaborate answer in marathi without any format."
