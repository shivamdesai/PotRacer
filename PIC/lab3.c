#include <p18f2455.h>
#include "configs.h"
#include "usb_defs.h"

#define	SHOW_ENUM_STATUS 1

#define	READ_POT			0x01		// vendor-specific request to read potentiometers
#define	READ_BUTTON			0x02		// vendor-specific request to read buttons
#define SET_LED				0x03		// vendor-specific request to set LEDs
#define CLEAR_LED			0x04		// vendor-specific request to clear LEDs

#define P0_POT PORTAbits.RA0
#define P1_POT PORTAbits.RA1
#define P0_BUTTON PORTAbits.RA2
#define P1_BUTTON PORTAbits.RA3
#define P0_LED PORTAbits.RA4
#define P1_LED PORTAbits.RA5

#pragma udata
BUFDESC USB_buffer_desc;
unsigned char USB_buffer_data[8];
unsigned char USB_error_flags;
unsigned char USB_curr_config;
unsigned char USB_device_status;
unsigned char USB_dev_req;
unsigned char USB_address_pending;
unsigned char rom *USB_desc_ptr;
unsigned char USB_bytes_left;
unsigned char USB_packet_length;
unsigned char USB_USTAT;
unsigned char USB_USWSTAT;

#pragma romdata
rom const unsigned char Device[] = {
	0x12,	// bLength
	DEVICE,	// bDescriptorType
	0x10,	// bcdUSB (low byte)
	0x01,	// bcdUSB (high byte)
	0x00,	// bDeviceClass
	0x00,	// bDeviceSubClass
	0x00,	// bDeviceProtocol
	MAX_PACKET_SIZE,	// bMaxPacketSize
	0x66,	// idVendor (low byte)
	0x66,	// idVendor (high byte)
	0x03,	// idProduct (low byte)
	0x00,	// idProduct (high byte)
	0x00,	// bcdDevice (low byte)
	0x00,	// bcdDevice (high byte)
	0x01,	// iManufacturer
	0x02,	// iProduct
	0x00,	// iSerialNumber (none)
	NUM_CONFIGURATIONS	// bNumConfigurations
};

rom const unsigned char Configuration1[] = {
	0x09,	// bLength
	CONFIGURATION,	// bDescriptorType
	0x12,	// wTotalLength (low byte)
	0x00,	// wTotalLength (high byte)
	NUM_INTERFACES,	// bNumInterfaces
	0x01,	// bConfigurationValue
	0x00,	// iConfiguration (none)
	0xA0,	// bmAttributes
	0x32,	// bMaxPower (100 mA)
	0x09,	// bLength (Interface1 descriptor starts here)
	INTERFACE,	// bDescriptorType
	0x00,	// bInterfaceNumber
	0x00,	// bAlternateSetting
	0x00,	// bNumEndpoints (excluding EP0)
	0xFF,	// bInterfaceClass (vendor specific class code)
	0x00,	// bInterfaceSubClass
	0xFF,	// bInterfaceProtocol (vendor specific protocol used)
	0x00	// iInterface (none)
};

rom const unsigned char String0[] = {
	0x04,	// bLength
	STRING,	// bDescriptorType
	0x09,	// wLANGID[0] (low byte)
	0x04	// wLANGID[0] (high byte)
};

rom const unsigned char String1[] = {
	0x34,	// bLength
	STRING,	// bDescriptorType
	'P', 0x00, 'r', 0x00, 'i', 0x00, 'n', 0x00, 'c', 0x00, 'i', 0x00, 'p', 0x00, 'l', 0x00, 'e', 0x00, 's', 0x00, ' ', 0x00,
	'o', 0x00, 'f', 0x00, ' ', 0x00,
	'E', 0x00, 'n', 0x00, 'g', 0x00, 'i', 0x00, 'n', 0x00, 'e', 0x00, 'e', 0x00, 'r', 0x00, 'i', 0x00, 'n', 0x00, 'g', 0x00
};

rom const unsigned char String2[] = {
	0x32,	// bLength
	STRING,	// bDescriptorType
	'E', 0x00, 'N', 0x00, 'G', 0x00, 'R', 0x00, ' ', 0x00, '2', 0x00, '2', 0x00, '1', 0x00, '0', 0x00, ' ', 0x00,
	'L', 0x00, 'a', 0x00, 'b', 0x00, ' ', 0x00, '3', 0x00, ' ', 0x00,
	'F', 0x00, 'i', 0x00, 'r', 0x00, 'm', 0x00, 'w', 0x00, 'a', 0x00, 'r', 0x00, 'e', 0x00
};

#pragma code
void InitUSB(void) {
	UIE = 0x00;					// mask all USB interrupts
	UIR = 0x00;					// clear all USB interrupt flags
	UCFG = 0x10;				// configure USB for low-speed transfers and to use the on-chip transciever and pull-up resistor
	UCON = 0x08;				// enable the USB module and its supporting circuitry
	USB_curr_config = 0x00;
	USB_USWSTAT = 0x00;			// default to powered state
	USB_device_status = 0x01;
	USB_dev_req = NO_REQUEST;	// No device requests in process
#ifdef SHOW_ENUM_STATUS
	TRISB = 0x00;				// set all bits of PORTB as outputs
	PORTB = 0x01;				// set bit zero to indicate Powered status
#endif
	while (UCONbits.SE0);		// wait for the first SE0 to end
}

void ServiceUSB(void) {
	BUFDESC *buf_desc_ptr;

	if (UIRbits.UERRIF) {
		UEIR = 0x00;
	} else if (UIRbits.SOFIF) {
		UIRbits.SOFIF = 0;
	} else if (UIRbits.IDLEIF) {
		UIRbits.IDLEIF = 0;
		UCONbits.SUSPND = 1;
#ifdef SHOW_ENUM_STATUS
		PORTB &= 0xE0;
		PORTBbits.RB4 = 1;
#endif
	} else if (UIRbits.ACTVIF) {
		UIRbits.ACTVIF = 0;
		UCONbits.SUSPND = 0;
#ifdef SHOW_ENUM_STATUS
		PORTB &= 0xE0;
		PORTB |= 0x01<<USB_USWSTAT;
#endif
	} else if (UIRbits.STALLIF) {
		UIRbits.STALLIF = 0;
	} else if (UIRbits.URSTIF) {
		USB_curr_config = 0x00;
		UIRbits.TRNIF = 0;		// clear TRNIF four times to clear out the USTAT FIFO
		UIRbits.TRNIF = 0;
		UIRbits.TRNIF = 0;
		UIRbits.TRNIF = 0;
		UEP0 = 0x00;				// clear all EP control registers to disable all endpoints
		UEP1 = 0x00;
		UEP2 = 0x00;
		UEP3 = 0x00;
		UEP4 = 0x00;
		UEP5 = 0x00;
		UEP6 = 0x00;
		UEP7 = 0x00;
		UEP8 = 0x00;
		UEP9 = 0x00;
		UEP10 = 0x00;
		UEP11 = 0x00;
		UEP12 = 0x00;
		UEP13 = 0x00;
		UEP14 = 0x00;
		UEP15 = 0x00;
		BD0O.bytecount = MAX_PACKET_SIZE;
		BD0O.address = EP0_OUT_buffer;	// EP0 OUT gets a buffer
		BD0O.status = 0x88;				// set UOWN bit (USB can write)
		BD0I.address = EP0_IN_buffer;	// EP0 IN gets a buffer
		BD0I.status = 0x08;				// clear UOWN bit (MCU can write)
		UADDR = 0x00;				// set USB Address to 0
		UIR = 0x00;				// clear all the USB interrupt flags
		UEP0 = ENDPT_CONTROL;	// EP0 is a control pipe and requires an ACK
		UEIE = 0xFF;			// enable all error interrupts
		USB_USWSTAT = DEFAULT_STATE;
		USB_device_status = 0x01;	// self powered, remote wakeup disabled
#ifdef SHOW_ENUM_STATUS
		PORTB &= 0xE0;
		PORTBbits.RB1 = 1;		// set bit 1 of PORTB to indicate Powered state
#endif
	} else if (UIRbits.TRNIF) {
		buf_desc_ptr = (BUFDESC *)((unsigned char *)(&BD0O)+(USTAT&0x7C));	// mask out bits 0, 1, and 7 of USTAT for offset into the buffer descriptor table
		USB_buffer_desc.status = buf_desc_ptr->status;
		USB_buffer_desc.bytecount = buf_desc_ptr->bytecount;
		USB_buffer_desc.address = buf_desc_ptr->address;
		USB_USTAT = USTAT;		// save the USB status register
		UIRbits.TRNIF = 0;		// clear TRNIF interrupt flag
#ifdef SHOW_ENUM_STATUS
		switch (USB_USTAT&0x18) {	// toggle bit 5, 6, or 7 of PORTB to reflect EP0, EP1, or EP2 activity
			case EP0:
				PORTB ^= 0x20;
				break;
			case EP1:
				PORTB ^= 0x40;
				break;
			case EP2:
				PORTB ^= 0x80;
		}
#endif
		USB_error_flags = 0x00;	// clear USB error flags
		switch (USB_buffer_desc.status&0x3C) {	// extract PID bits
			case TOKEN_SETUP:
				ProcessSetupToken();
				break;
			case TOKEN_IN:
				ProcessInToken();
				break;
			case TOKEN_OUT:
				ProcessOutToken();
		}
		if (USB_error_flags&0x01) {		// if there was a Request Error...
			BD0O.bytecount = MAX_PACKET_SIZE;	// ...get ready to receive the next Setup token...
			BD0I.status = 0x84;
			BD0O.status = 0x84;					// ...and issue a protocol stall on EP0
		}
	}
}


void ProcessSetupToken(void) {
	unsigned char n;

	for (n = 0; n<8; n++) {
		USB_buffer_data[n] = USB_buffer_desc.address[n];
	}
	BD0O.bytecount = MAX_PACKET_SIZE;	// reset the EP0 OUT byte count
	BD0I.status = 0x08;			// return the EP0 IN buffer to us (dequeue any pending requests)
	BD0O.status = (!(USB_buffer_data[bmRequestType]&0x80) && (USB_buffer_data[wLength] || USB_buffer_data[wLengthHigh])) ? 0xC8:0x88;	// set EP0 OUT UOWN back to USB and DATA0/DATA1 packet according to the request type
	UCONbits.PKTDIS = 0;			// assuming there is nothing to dequeue, clear the packet disable bit
	USB_dev_req = NO_REQUEST;		// clear the device request in process
	switch (USB_buffer_data[bmRequestType]&0x60) {	// extract request type bits
		case STANDARD:
			StandardRequests();
			break;
		case CLASS:
			ClassRequests();
			break;
		case VENDOR:
			VendorRequests();
			break;
		default:
			USB_error_flags |= 0x01;	// set Request Error Flag
	}
}

void StandardRequests(void) {
	unsigned char *UEP;
	unsigned char n;
	BUFDESC *buf_desc_ptr;

	switch (USB_buffer_data[bRequest]) {
		case GET_STATUS:
			switch (USB_buffer_data[bmRequestType]&0x1F) {	// extract request recipient bits
				case RECIPIENT_DEVICE:
					BD0I.address[0] = USB_device_status;
					BD0I.address[1] = 0x00;
					BD0I.bytecount = 0x02;
					BD0I.status = 0xC8;		// send packet as DATA1, set UOWN bit
					break;
				case RECIPIENT_INTERFACE:
					switch (USB_USWSTAT) {
						case ADDRESS_STATE:
							USB_error_flags |= 0x01;	// set Request Error Flag
							break;
						case CONFIG_STATE:
							if (USB_buffer_data[wIndex]<NUM_INTERFACES) {
								BD0I.address[0] = 0x00;
								BD0I.address[1] = 0x00;
								BD0I.bytecount = 0x02;
								BD0I.status = 0xC8;		// send packet as DATA1, set UOWN bit
							} else {
								USB_error_flags |= 0x01;	// set Request Error Flag
							}
					}
					break;
				case RECIPIENT_ENDPOINT:
					switch (USB_USWSTAT) {
						case ADDRESS_STATE:
							if (!(USB_buffer_data[wIndex]&0x0F)) {	// get EP, strip off direction bit and see if it is EP0
								BD0I.address[0] = (((USB_buffer_data[wIndex]&0x80) ? BD0I.status:BD0O.status)&0x04)>>2;	// return the BSTALL bit of EP0 IN or OUT, whichever was requested
								BD0I.address[1] = 0x00;
								BD0I.bytecount = 0x02;
								BD0I.status = 0xC8;		// send packet as DATA1, set UOWN bit
							} else {
								USB_error_flags |= 0x01;	// set Request Error Flag
							}
							break;
						case CONFIG_STATE:
							UEP = (unsigned char *)&UEP0;
							n = USB_buffer_data[wIndex]&0x0F;	// get EP and strip off direction bit for offset from UEP0
							buf_desc_ptr = &BD0O+((n<<1)|((USB_buffer_data[wIndex]&0x80) ? 0x01:0x00));	// compute pointer to the buffer descriptor for the specified EP
							if (UEP[n]&((USB_buffer_data[wIndex]&0x80) ? 0x02:0x04)) { // if the specified EP is enabled for transfers in the specified direction...
								BD0I.address[0] = ((buf_desc_ptr->status)&0x04)>>2;	// ...return the BSTALL bit of the specified EP
								BD0I.address[1] = 0x00;
								BD0I.bytecount = 0x02;
								BD0I.status = 0xC8;		// send packet as DATA1, set UOWN bit
							} else {
								USB_error_flags |= 0x01;	// set Request Error Flag
							}
							break;
						default:
							USB_error_flags |= 0x01;	// set Request Error Flag
					}
					break;
				default:
					USB_error_flags |= 0x01;	// set Request Error Flag
			}
			break;
		case CLEAR_FEATURE:
		case SET_FEATURE:
			switch (USB_buffer_data[bmRequestType]&0x1F) {	// extract request recipient bits
				case RECIPIENT_DEVICE:
					switch (USB_buffer_data[wValue]) {
						case DEVICE_REMOTE_WAKEUP:
							if (USB_buffer_data[bRequest]==CLEAR_FEATURE)
								USB_device_status &= 0xFE;
							else
								USB_device_status |= 0x01;
							BD0I.bytecount = 0x00;		// set EP0 IN byte count to 0
							BD0I.status = 0xC8;		// send packet as DATA1, set UOWN bit
							break;
						default:
							USB_error_flags |= 0x01;	// set Request Error Flag
					}
					break;
				case RECIPIENT_ENDPOINT:
					switch (USB_USWSTAT) {
						case ADDRESS_STATE:
							if (!(USB_buffer_data[wIndex]&0x0F)) {	// get EP, strip off direction bit, and see if its EP0
								BD0I.bytecount = 0x00;		// set EP0 IN byte count to 0
								BD0I.status = 0xC8;		// send packet as DATA1, set UOWN bit
							} else {
								USB_error_flags |= 0x01;	// set Request Error Flag
							}
							break;
						case CONFIG_STATE:
							UEP = (unsigned char *)&UEP0;
							if (n = USB_buffer_data[wIndex]&0x0F) {	// get EP and strip off direction bit for offset from UEP0, if not EP0...
								buf_desc_ptr = &BD0O+((n<<1)|((USB_buffer_data[wIndex]&0x80) ? 0x01:0x00));	// compute pointer to the buffer descriptor for the specified EP
								if (USB_buffer_data[wIndex]&0x80) {	// if the specified EP direction is IN...
									if (UEP[n]&0x02) {	// if EPn is enabled for IN transfers...
										buf_desc_ptr->status = (USB_buffer_data[bRequest]==CLEAR_FEATURE) ? 0x00:0x84;
									} else {
										USB_error_flags |= 0x01;	// set Request Error Flag
									}
								} else {	// ...otherwise the specified EP direction is OUT, so...
									if (UEP[n]&0x04) {	// if EPn is enabled for OUT transfers...
										buf_desc_ptr->status = (USB_buffer_data[bRequest]==CLEAR_FEATURE) ? 0x88:0x84;
									} else {
										USB_error_flags |= 0x01;	// set Request Error Flag
									}
								}
							}
							if (!(USB_error_flags&0x01)) {	// if there was no Request Error...
								BD0I.bytecount = 0x00;
								BD0I.status = 0xC8;		// ...send packet as DATA1, set UOWN bit
							}
							break;
						default:
							USB_error_flags |= 0x01;	// set Request Error Flag
					}
					break;
				default:
					USB_error_flags |= 0x01;	// set Request Error Flag
			}
			break;
		case SET_ADDRESS:
			if (USB_buffer_data[wValue]>0x7F) {	// if new device address is illegal, send Request Error
				USB_error_flags |= 0x01;	// set Request Error Flag
			} else {
				USB_dev_req = SET_ADDRESS;	// processing a SET_ADDRESS request
				USB_address_pending = USB_buffer_data[wValue];	// save new address
				BD0I.bytecount = 0x00;		// set EP0 IN byte count to 0
				BD0I.status = 0xC8;		// send packet as DATA1, set UOWN bit
			}
			break;
		case GET_DESCRIPTOR:
			USB_dev_req = GET_DESCRIPTOR;	// processing a GET_DESCRIPTOR request
			switch (USB_buffer_data[wValueHigh]) {
				case DEVICE:
					USB_desc_ptr = Device;
					USB_bytes_left = USB_desc_ptr[0];
					if ((USB_buffer_data[wLengthHigh]==0x00) && (USB_buffer_data[wLength]<USB_bytes_left)) {
						USB_bytes_left = USB_buffer_data[wLength];
					}
					SendDescriptorPacket();
					break;
				case CONFIGURATION:
					switch (USB_buffer_data[wValue]) {
						case 0:
							USB_desc_ptr = Configuration1;
							break;
						default:
							USB_error_flags |= 0x01;	// set Request Error Flag
					}
					if (!(USB_error_flags&0x01)) {
						USB_bytes_left = USB_desc_ptr[2];	// wTotalLength at an offset of 2
						if ((USB_buffer_data[wLengthHigh]==0x00) && (USB_buffer_data[wLength]<USB_bytes_left)) {
							USB_bytes_left = USB_buffer_data[wLength];
						}
						SendDescriptorPacket();
					}
					break;
				case STRING:
					switch (USB_buffer_data[wValue]) {
						case 0:
							USB_desc_ptr = String0;
							break;
						case 1:
							USB_desc_ptr = String1;
							break;
						case 2:
							USB_desc_ptr = String2;
							break;
						default:
							USB_error_flags |= 0x01;	// set Request Error Flag
					}
					if (!(USB_error_flags&0x01)) {
						USB_bytes_left = USB_desc_ptr[0];
						if ((USB_buffer_data[wLengthHigh]==0x00) && (USB_buffer_data[wLength]<USB_bytes_left)) {
							USB_bytes_left = USB_buffer_data[wLength];
						}
						SendDescriptorPacket();
					}
					break;
				default:
					USB_error_flags |= 0x01;	// set Request Error Flag
			}
			break;
		case GET_CONFIGURATION:
			BD0I.address[0] = USB_curr_config;	// copy current device configuration to EP0 IN buffer
			BD0I.bytecount = 0x01;
			BD0I.status = 0xC8;		// send packet as DATA1, set UOWN bit
			break;
		case SET_CONFIGURATION:
			if (USB_buffer_data[wValue]<=NUM_CONFIGURATIONS) {
				UEP1 = 0x00;	// clear all EP control registers except for EP0 to disable EP1-EP15 prior to setting configuration
				UEP2 = 0x00;
				UEP3 = 0x00;
				UEP4 = 0x00;
				UEP5 = 0x00;
				UEP6 = 0x00;
				UEP7 = 0x00;
				UEP8 = 0x00;
				UEP9 = 0x00;
				UEP10 = 0x00;
				UEP11 = 0x00;
				UEP12 = 0x00;
				UEP13 = 0x00;
				UEP14 = 0x00;
				UEP15 = 0x00;
				switch (USB_curr_config = USB_buffer_data[wValue]) {
					case 0:
						USB_USWSTAT = ADDRESS_STATE;
#ifdef SHOW_ENUM_STATUS
						PORTB &= 0xE0;
						PORTBbits.RB2 = 1;
#endif
						break;
					default:
						USB_USWSTAT = CONFIG_STATE;
#ifdef SHOW_ENUM_STATUS
						PORTB &= 0xE0;
						PORTBbits.RB3 = 1;
#endif
				}
				BD0I.bytecount = 0x00;		// set EP0 IN byte count to 0
				BD0I.status = 0xC8;		// send packet as DATA1, set UOWN bit
			} else {
				USB_error_flags |= 0x01;	// set Request Error Flag
			}
			break;
		case GET_INTERFACE:
			switch (USB_USWSTAT) {
				case CONFIG_STATE:
					if (USB_buffer_data[wIndex]<NUM_INTERFACES) {
						BD0I.address[0] = 0x00;	// always send back 0 for bAlternateSetting
						BD0I.bytecount = 0x01;
						BD0I.status = 0xC8;		// send packet as DATA1, set UOWN bit
					} else {
						USB_error_flags |= 0x01;	// set Request Error Flag
					}
					break;
				default:
					USB_error_flags |= 0x01;	// set Request Error Flag
			}
			break;
		case SET_INTERFACE:
			switch (USB_USWSTAT) {
				case CONFIG_STATE:
					if (USB_buffer_data[wIndex]<NUM_INTERFACES) {
						switch (USB_buffer_data[wValue]) {
							case 0:		// currently support only bAlternateSetting of 0
								BD0I.bytecount = 0x00;		// set EP0 IN byte count to 0
								BD0I.status = 0xC8;		// send packet as DATA1, set UOWN bit
								break;
							default:
								USB_error_flags |= 0x01;	// set Request Error Flag
						}
					} else {
						USB_error_flags |= 0x01;	// set Request Error Flag
					}
					break;
				default:
					USB_error_flags |= 0x01;	// set Request Error Flag
			}
			break;
		case SET_DESCRIPTOR:
		case SYNCH_FRAME:
		default:
			USB_error_flags |= 0x01;	// set Request Error Flag
	}
}

void ClassRequests(void) {
	switch (USB_buffer_data[bRequest]) {
		default:
			USB_error_flags |= 0x01;	// set Request Error Flag
	}
}

unsigned char get_pot(short pot) {
    // Reads from a specified potentiometer 'pot'
    // using analog to digital conversion
    if (pot)
        ADCON0 = 0b00000011;
    else
        ADCON0 = 0b00000111;
    while (ADCON0bits.GO_DONE==1) {}
    return ADRESH;
}

short get_button(short button) {
    // Reads from a specified button 'button'
    if (button)
        return P0_BUTTON;
    else
        return P1_BUTTON;
}

short set_LED(short led) {
    // Turns on the specified led 'led'
    if (led)
        P0_LED = 1;
    else
        P1_LED = 1;
}

short clear_LED(short led) {
    // Turns off the specified led 'led'
    if (led)
        P0_LED = 0;
    else
        P1_LED = 0;
}

// This function is called by ServiceUSB(), when a Vendor Request
// is received
void VendorRequests(void) {
    switch (USB_buffer_data[bRequest]) {
        case READ_POT:
            // When this request is received, send a message to
            // the computer, telling it the value of a potentiometer
            // specified by wValue in the usb_control_transfer request
            BD0I.address[0] = get_pot(USB_buffer_data[wValue]);
            BD0I.bytecount = 0x01;      // set EP0 IN byte count to 1
            BD0I.status = 0xC8;         // send packet as DATA1, set UOWN bit
            break;
        case READ_BUTTON:
            // When this request is received, send a message to
            // the computer, telling it the value of a button
            // specified by wValue in the usb_control_transfer request
            BD0I.address[0] = get_button(USB_buffer_data[wValue]);
            BD0I.bytecount = 0x01;      // set EP0 IN byte count to 1
            BD0I.status = 0xC8;         // send packet as DATA1, set UOWN bit
            break;
        case SET_LED:
            // When this request is received, turn on the LED
            // specified by wValue in the usb_control_transfer request
            set_LED(USB_buffer_data[wValue]);
            BD0I.bytecount = 0x00;      // set EP0 IN byte count to 1
            BD0I.status = 0xC8;         // send packet as DATA1, set UOWN bit
            break;
        case CLEAR_LED:
            // When this request is received, turn off the LED
            // specified by wValue in the usb_control_transfer request
            clear_LED(USB_buffer_data[wValue]);
            BD0I.bytecount = 0x00;      // set EP0 IN byte count to 1
            BD0I.status = 0xC8;         // send packet as DATA1, set UOWN bit
            break;
        default:
            USB_error_flags |= 0x01;    // set Request Error Flag
    }
}

void ProcessInToken(void) {
	switch (USB_USTAT&0x18) {	// extract the EP bits
		case EP0:
			switch (USB_dev_req) {
				case SET_ADDRESS:
					switch (UADDR = USB_address_pending) {
						case 0:
							USB_USWSTAT = DEFAULT_STATE;
#ifdef SHOW_ENUM_STATUS
							PORTB &= 0xE0;
							PORTBbits.RB1 = 1;
#endif
							break;
						default:
							USB_USWSTAT = ADDRESS_STATE;
#ifdef SHOW_ENUM_STATUS
							PORTB &= 0xE0;
							PORTBbits.RB2 = 1;
#endif
					}
					break;
				case GET_DESCRIPTOR:
					SendDescriptorPacket();
					break;
			}
			break;
		case EP1:
			break;
		case EP2:
			break;
	}
}

void ProcessOutToken(void) {
	switch (USB_USTAT&0x18) {	// extract the EP bits
		case EP0:
			BD0O.bytecount = MAX_PACKET_SIZE;
			BD0O.status = 0x88;
			BD0I.bytecount = 0x00;		// set EP0 IN byte count to 0
			BD0I.status = 0xC8;		// send packet as DATA1, set UOWN bit
			break;
		case EP1:
			break;
		case EP2:
			break;
	}
}

void SendDescriptorPacket(void) {
	unsigned char n;

	if (USB_bytes_left<MAX_PACKET_SIZE) {
		USB_dev_req = NO_REQUEST;	// sending a short packet, so clear device request
		USB_packet_length = USB_bytes_left;
		USB_bytes_left = 0x00;
	} else {
		USB_packet_length = MAX_PACKET_SIZE;
		USB_bytes_left -= MAX_PACKET_SIZE;
	}
	for (n = 0; n<USB_packet_length; n++) {
		BD0I.address[n] = *USB_desc_ptr++;
	}
	BD0I.bytecount = USB_packet_length;
	BD0I.status = ((BD0I.status^0x40)&0x40)|0x88; // toggle the DATA01 bit, clear the PIDs bits, and set the UOWN and DTS bits
}

void main(void) {
    unsigned char temp;

    PORTA = 0b00000000;      // clear all PORTA pins
    TRISA = 0b00001111;      // configure RA0..RA3 as inputs
                             // (the buttons and potentiometers)
    ADCON1 = 0b00001101;     // Configure the potentiometers to be
                             // analog, and the other pins to be digital
    ADCON2 = 0b00101110;     // configure A/D module result to left justified,
                             // acquisition time to 32 us,
                             // and clock period to 2.67 us
    InitUSB();               // initialize the USB registers and serial
                             // interface engine

    // service USB requests while the peripheral is not configured
    while (USB_USWSTAT != CONFIG_STATE) {
        ServiceUSB();
    }

    while (1) {
        ServiceUSB(); // service any pending USB requests
    }
}
