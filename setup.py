from setuptools import setup, find_packages

setup(
    name="mcp_workflow_system",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"":"src"},
    install_requires=[
        "spacy>=3.6.0",
        "networkx>=3.1",
        "pydantic>=2.4.0",
    ],
    python_requires=">=3.10",
    author="Omar El Mountassir",
    author_email="omar.mountassir@gmail.com",
    description="Intelligent workflow system using Model Context Protocol",
    keywords="ai, knowledge-graph, nlp, mcp",
    url="https://github.com/omar-el-mountassir/mcp-workflow-system",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
)
