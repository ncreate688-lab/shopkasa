import re

with open(r'c:\Users\HP\Desktop\projects\soft-build-web-main\soft-build-web-main\src\App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# The wrapper has the issue on line 4677: `{!hideTitle && <h2 className="text-2xl font-bold text-slate-800">Business Analytics</h2>}`
# We want to replace only the occurrence inside BusinessAnalyticsWrapper.
# We can find the definition of BusinessAnalyticsWrapper and fix it.

wrapper_pattern = r'const BusinessAnalyticsWrapper = \(props\) => \{([\s\S]*?)<div className="flex border-b border-slate-200'
def replacer(match):
    fixed = match.group(1).replace('{!hideTitle && <h2', '<h2').replace('Analytics</h2>}', 'Analytics</h2>')
    return 'const BusinessAnalyticsWrapper = (props) => {' + fixed + '<div className="flex border-b border-slate-200'

content = re.sub(wrapper_pattern, replacer, content)

with open(r'c:\Users\HP\Desktop\projects\soft-build-web-main\soft-build-web-main\src\App.jsx', 'w', encoding='utf-8') as f:
    f.write(content)
print('Fixed')
