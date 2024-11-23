export function decryptMessage(messageString: string) {
	let decryptedText = '';
	let shift = 3;

	if (messageString == 'usb drive not found') {
		return messageString;
	}

	for (let char of messageString) {
		if (/[a-zA-Z]/.test(char)) {
			const shiftBase = char === char.toUpperCase() ? 'A'.charCodeAt(0) : 'a'.charCodeAt(0);
			const decryptedChar = String.fromCharCode(
				((char.charCodeAt(0) - shiftBase - shift + 26) % 26) + shiftBase
			);
			decryptedText += decryptedChar;
		} else {
			decryptedText += char;
		}
	}

	return decryptedText;
}

export interface UsbData {
	permission: string;
	email: string;
	password: string;
}

export async function fetchUsbMessage(): Promise<UsbData | undefined> {
	try {
		const response = await fetch('http://127.0.0.1:5000/message');
		if (!response.ok) {
			throw new Error('Network response was not ok');
		}
		const data = await response.json() as UsbData;
		return data;
	} catch (error) {
		console.error('Error:', error);
	}
}