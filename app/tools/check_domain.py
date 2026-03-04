import dns.resolver
from langchain_core.tools import tool

@tool
def check_domain(domain: str) -> str:
    """
    Performs a deep DNS analysis of the given domain.
    """

    report = ""  # Initialize the report

    try:
        # Extract the domain from an email address if necessary
        domain_validate = domain.split("@")[-1].strip() if "@" in domain else domain.strip()
    except Exception as e:
        return f"Error processing the domain: {str(e)}"

    try:
        # Check the A record
        try:
            dns.resolver.resolve(domain_validate, 'A')
            report += "A record: Found\n"
        except dns.resolver.NoAnswer:
            report += "A record: Not found\n"

        # Check the MX record
        try:
            dns.resolver.resolve(domain_validate, 'MX')
            report += "MX record: Found\n"
        except dns.resolver.NoAnswer:
            report += "MX record: Not found\n"

        # Check the TXT record
        try:
            dns.resolver.resolve(domain_validate, 'TXT')
            report += "TXT record: Found\n"
        except dns.resolver.NoAnswer:
            report += "TXT record: Not found\n"

    except Exception as e:
        return f"Error during DNS resolution: {str(e)}"

    return report