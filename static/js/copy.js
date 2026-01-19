document.querySelectorAll('pre').forEach(block => {
    // Only add button if the block doesn't have one
    if (!block.querySelector('.copy-btn')) {
        const button = document.createElement('button');
        button.innerText = 'Copy';
        button.className = 'copy-btn';

        button.onclick = () => {
            // Get text from the <code> tag inside <pre>, or the <pre> itself
            const codeElement = block.querySelector('code') || block;
            const textToCopy = codeElement.innerText;

            navigator.clipboard.writeText(textToCopy).then(() => {
                button.innerText = 'Copied!';
                button.classList.add('copied');
                
                setTimeout(() => {
                    button.innerText = 'Copy';
                    button.classList.remove('copied');
                }, 1500);
            });
        };

        // Ensure the pre block is positioned relative so the button can be absolute
        block.style.position = 'relative';
        block.appendChild(button);
    }
});