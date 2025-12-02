from setuptools import setup, find_packages

setup(
    name="mock-interview-evaluator",
    version="1.0.0",
    description="AI-powered mock interview evaluation platform",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "streamlit>=1.29.0",
        "groq>=0.4.1",
        "SpeechRecognition>=3.10.0",
        "opencv-python>=4.8.1.78",
        "numpy>=1.24.3",
        "Pillow>=10.1.0",
        "PyAudio>=0.2.14",
        "python-dotenv>=1.0.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)