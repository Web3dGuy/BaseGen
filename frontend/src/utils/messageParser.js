// messageParser.js
const URL_REGEX = /(https?:\/\/[^\s<]+[^<.,:;"')\]\s])/g;
const IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.webp'];

export function parseMessage(text) {
    const parts = [];
    let lastIndex = 0;

    // Find all URLs in the text
    const matches = Array.from(text.matchAll(URL_REGEX));
    
    matches.forEach(match => {
        const [url] = match;
        const startIndex = match.index;
        
        // Add text before the URL
        if (startIndex > lastIndex) {
            parts.push({
                type: 'text',
                content: text.slice(lastIndex, startIndex)
            });
        }
        
        // Check if URL is an image
        const isImage = IMAGE_EXTENSIONS.some(ext => 
            url.toLowerCase().endsWith(ext)
        );
        
        // Add the URL/image
        parts.push({
            type: isImage ? 'image' : 'link',
            content: url
        });
        
        lastIndex = startIndex + url.length;
    });
    
    // Add remaining text
    if (lastIndex < text.length) {
        parts.push({
            type: 'text',
            content: text.slice(lastIndex)
        });
    }
    
    return parts;
}

export function sanitizeMessage(text) {
    // Basic XSS protection
    return text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}
