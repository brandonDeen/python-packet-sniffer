'''
Jesus Linares
Brandon Deen
Mariana Flores
Geoff Lyle

Description:
This Linux and Windows application processes packets in the local network and displays
	the supported protocol's header and data.
Linux has support for link layer whereas Windows has support for network layer.
The header is displayed in the same format(s) wireshark displays them.
'''

import socket, sys, time, platform
from struct import *

# Constants for each header length.
constEthHeaderLength = 14
constARPLength = 28
constIPHeaderLength = 20
constTCPHeaderLength = 20
constUDPHeaderLength = 8
constICMPHeaderLength = 8

def eth(packet, begin, end):
	# Get Ethernet header using begin and end.
	ethHeader = packet[begin:end]

	# Unpack the header because it originally in hex.
	# The regular expression helps unpack the header.
	# ! signifies we are unpacking a network endian.
	# 6s signifies we are unpacking a string of size 6 bytes.
	# H signifies we are unpacking an integer of size 2 bytes.
	ethHeaderUnpacked = unpack('!6s6sH', ethHeader)
	
	# The first 6s is 6 bytes and contains the destination address.
	ethDestAddress = ethHeaderUnpacked[0]
	
	# The second 6s is 6 bytes and contains the source address.
	ethSourceAddress = ethHeaderUnpacked[1]
	
	# The third H is 2 bytes and contains the packet length.
	ethType = socket.ntohs(ethHeaderUnpacked[2])
	
	# Properly unpack and format the destination address.
	ethDestAddress = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (ord(ethDestAddress[0]), ord(ethDestAddress[1]), ord(ethDestAddress[2]), ord(ethDestAddress[3]), ord(ethDestAddress[4]), ord(ethDestAddress[5]))
	
	# Properly unpack and format the source address.
	ethSourceAddress = "%.2x:%.2x:%.2x:%.2x:%.2x:%.2x" % (ord(ethSourceAddress[0]), ord(ethSourceAddress[1]), ord(ethSourceAddress[2]), ord(ethSourceAddress[3]), ord(ethSourceAddress[4]), ord(ethSourceAddress[5]))
	
	# Print Ethernet Header
	print('\n********************\n** Ethernet (MAC) **\n********************' +
	'\nDestination Address: ' + str(ethDestAddress) +
	'\nSource Address: ' + str(ethSourceAddress) +
	'\nEtherType: ' + str(ethType))
	
	return ethType
	
def arp(packet, begin, end):
	'''
	Need ARP support
	'''
	# Print Ethernet Header
	print('\n*******************\n******** ARP ********\n*******************')

def ip(packet, begin, end):
	# Get IP header using begin and end.	
	ipHeader = packet[begin:end]

	# Unpack the header because it originally in hex.
	# The regular expression helps unpack the header.
	# ! signifies we are unpacking a network endian.
	# B signifies we are unpacking an integer of size 1 byte.
	# H signifies we are unpacking an integer of size 2 bytes.
	# 4s signifies we are unpacking a string of size 4 bytes.
	ipHeaderUnpacked = unpack('!BBHHHBBH4s4s' , ipHeader)
	
	# The first B is 1 byte and contains the version and header length.
	# Both are 4 bits each, split ipHeaderUnpacked[0] in "half".
	ipVersionAndHeaderLength = ipHeaderUnpacked[0]
	ipVersion = ipVersionAndHeaderLength >> 4
	ipHeaderLength = ipVersionAndHeaderLength & 0xF

	# The second B is 1 byte and contains the service type and ECN.
	ipDSCPAndECN = ipHeaderUnpacked[1]
	ipDSCP = ipDSCPAndECN >> 2
	ipECN = ipDSCPAndECN & 0x3

	# The first H is 2 bytes and contains the total length.
	ipTotalLength = ipHeaderUnpacked[2]

	# The second H is 2 bytes and contains the total length.
	ipIdentification = ipHeaderUnpacked[3]

	# The third H is 2 bytes and contains the flags and fragment offset.
	# Flags is 3 bits and fragment offset is 13 bits.
	# Split ipHeaderUnpacked[4].
	ipFlagsAndFragmentOffset = ipHeaderUnpacked[4]
	ipFlags = ipFlagsAndFragmentOffset >> 13
	ipFragmentOffset = ipFlagsAndFragmentOffset & 0x1FFF

	# The third B is 1 byte and contains the time to live.
	ipTimeToLive = ipHeaderUnpacked[5]
	
	# Our fourth B is 1 byte and contains the protocol.
	ipProtocol = ipHeaderUnpacked[6]
	
	# The fourth H is 2 bytes and contains the header checksum.
	ipHeaderChecksum = ipHeaderUnpacked[7]

	# The first 4s is 4 bytes and contains the source address.
	ipSourceAddress = socket.inet_ntoa(ipHeaderUnpacked[8]);

	# The second 4s is 4 bytes and contains the dest address.
	ipDestAddress = socket.inet_ntoa(ipHeaderUnpacked[9]);

	# Print IP Header
	# Some segments of the header are switched back to hex form because that
	# 	is the format wireshark has it.
	print('\n********************\n******** IP ********\n********************' + 
		'\nVersion: ' + str(ipVersion) +
		'\nHeader Length: ' + str(ipHeaderLength) + ' 32-bit words' +
		'\nDifferentiated Services Code Point: ' + format(ipDSCP, '#04X') + ' , ' + str(ipDSCP) +
		'\nExplicit Congestion Notification: ' + format(ipECN, '#04X') + ' , ' + str(ipECN) +
		'\nTotal Length: ' + str(ipTotalLength) + ' bytes' + 
		'\nIdentification: ' + format(ipIdentification, '#04X') + ' , ' + str(ipIdentification) +
		'\nFlags: ' + format(ipFlags, '#04X') + ' , ' + str(ipFlags) +
		'\nFragment Offset: ' + str(ipFragmentOffset) + ' eight-byte blocks' +
		'\nTime to Live: ' + str(ipTimeToLive) + ' seconds' +
		'\nProtocol: ' + str(ipProtocol) +
		'\nHeader Checksum: ' + format(ipHeaderChecksum, '#04X') + 
		'\nSource Address: ' + str(ipSourceAddress) +
		'\nDestination Address: ' + str(ipDestAddress))
	
	return ipProtocol

def icmp(packet, begin, end):
	# Get ICMP header using begin and end.
	icmpHeader = packet[begin:end]

	# Unpack the header because it originally in hex.
	# The regular expression helps unpack the header.
	# ! signifies we are unpacking a network endian.
	# B signifies we are unpacking an integer of size 1 byte.
	# H signifies we are unpacking an integer of size 2 bytes.
	# L signifies we are unpacking a long of size 4 bytes.
	icmpHeaderUnpacked = unpack('!BBHL', icmpHeader)

	# The first B is 1 byte and contains the type.
	icmpType = icmpHeaderUnpacked[0]

	# The second B is 1 byte and contains the code.
	icmpCode = icmpHeaderUnpacked[1]

	# The first H is 2 bytes and contains the checksum.
	icmpChecksum = icmpHeaderUnpacked[2]

	# Check if the type is 1 or 8, if so, unpack the identifier and sequence number.
	if (icmpType == 0) or (icmpType == 8):
		# The first L is 4 bytes and contains the rest of the header.
		icmpIdentifier = icmpHeaderUnpacked[3] >> 16
		icmpSeqNumber = icmpHeaderUnpacked[3] & 0xFFFF
		
		# Print ICMP Header
		# Some segments of the header are switched back to hex form because that
		# 	is the format wireshark has it.
		print('\n********************\n******* ICMP *******\n********************' +
			'\nType: ' + str(icmpType) +
			'\nCode: ' + str(icmpCode) + 
			'\nChecksum: ' + format(icmpChecksum, '#04X') + 
			'\nIdentifier: ' + str(icmpIdentifier) +
			'\nSequence Number: ' + str(icmpSeqNumber))
	# If not, just print out everything but the last L.
	else:
		print('\n********************\n******* ICMP *******\n********************' +
			'\nType: ' + str(icmpType) +
			'\nCode: ' + str(icmpCode) + 
			'\nChecksum: ' + format(icmpChecksum, '#04X'))

def tcp(packet, begin, end):
	# Get TCP header using begin and end.
	tcpHeader = packet[begin:end]

	# Unpack the header because it originally in hex.
	# The regular expression helps unpack the header.
	# ! signifies we are unpacking a network endian.
	# H signifies we are unpacking an integer of size 2 bytes.
	# L signifies we are unpacking a long of size 4 bytes.
	# B signifies we are unpacking an integer of size 1 byte.
	tcpHeaderUnpacked = unpack('!HHLLBBHHH', tcpHeader)
	
	# The first H is 2 bytes and contains the source port.
	tcpSourcePort = tcpHeaderUnpacked[0]
	
	# The second H is 2 bytes and contains the destination port.
	tcpDestPort = tcpHeaderUnpacked[1]

	# The first L is 2 bytes and contains the sequence number.
	tcpSeqNumber = tcpHeaderUnpacked[2]
	
	# The second L is 4 bytes and contains the acknowledgement number.
	tcpAckNumber = tcpHeaderUnpacked[3]
	
	# The first B is 1 byte and contains the data offset, reserved bits, and NS flag.
	# Split tcpHeaderUnpacked[4]
	tcpDataOffsetAndReserved = tcpHeaderUnpacked[4]
	tcpDataOffset = tcpDataOffsetAndReserved >> 4
	tcpReserved = (tcpDataOffsetAndReserved >> 1) & 0x7
	tcpNSFlag = tcpDataOffsetAndReserved & 0x1
	
	# The second B is 1 byte and contains the rest of the flags.
	# Split tcpHeaderUnpacked[5].
	tcpRestOfFLags = tcpHeaderUnpacked[5]
	tcpCWRFlag = tcpRestOfFLags >> 7
	tcpECEFlag = (tcpRestOfFLags >> 6) & 0x1
	tcpURGFlag = (tcpRestOfFLags >> 5) & 0x1
	tcpACKFlag = (tcpRestOfFLags >> 4) & 0x1
	tcpPSHFlag = (tcpRestOfFLags >> 3) & 0x1
	tcpRSTFlag = (tcpRestOfFLags >> 2) & 0x1
	tcpSYNFlag = (tcpRestOfFLags >> 1) & 0x1
	tcpFINFlag = tcpRestOfFLags & 0x1
	
	# The third H is 2 bytes and contains the window size.
	tcpWindowSize = tcpHeaderUnpacked[6]
	
	# The fourth H is 2 byte and conntains the checksum.
	tcpChecksum = tcpHeaderUnpacked[7]
	
	# The fifth H is 2 bytes and constains the urgent pointer.
	tcpUrgentPointer = tcpHeaderUnpacked[8]
	
	# Print TCP Header
	# Some segments of the header are switched back to hex form because that
	# 	is the format wireshark has it.
	print('\n*******************\n******* TCP *******\n*******************' +
	'\nSource Port: ' + str(tcpSourcePort) +
	'\nDestination Port: ' + str(tcpDestPort) +
	'\nSequence Number: ' + str(tcpSeqNumber) +
	'\nAcknowledgment Number: ' + str(tcpAckNumber) +
	'\nData Offset: ' + str(tcpDataOffset) + ' 32-bit words' +
	'\nReserved: ' + format(tcpReserved, '03b') + '. .... ....'
	'\nNS Flag:  ' + '...' + format(tcpNSFlag, '01b') + ' .... ....' +
	'\nCWR Flag: ' + '.... ' + format(tcpCWRFlag, '01b') + '... ....' +
	'\nECE Flag: ' + '.... .' + format(tcpECEFlag, '01b') + '.. ....' +
	'\nURG Flag: ' + '.... ..' + format(tcpURGFlag, '01b') + '. ....' +
	'\nACK Flag: ' + '.... ...' + format(tcpACKFlag, '01b') + ' ....' +
	'\nPSH Flag: ' + '.... .... ' + format(tcpPSHFlag, '01b') + '...' +
	'\nRST Flag: ' + '.... .... .' + format(tcpRSTFlag, '01b') + '..' +
	'\nSYN Flag: ' + '.... .... ..' + format(tcpSYNFlag, '01b') + '.' +
	'\nFIN Flag: ' + '.... .... ...' + format(tcpFINFlag, '01b') +
	'\nWindow Size: ' + str(tcpWindowSize) + ' bytes' +
	'\nUrgent Pointer: ' + str(tcpUrgentPointer) +
	'\nChecksum: ' + format(tcpChecksum, '#04X'))

def udp(packet, begin, end):
	# Get UDP header using begin and end.
	udpHeader = packet[begin:end]

	# Unpack the header because it originally in hex.
	# The regular expression helps unpack the header.
	# ! signifies we are unpacking a network endian.
	# H signifies we are unpacking an integer of size 2 bytes.
	udpHeaderUnpacked = unpack('!HHHH', udpHeader)
	 
	# The first H is 2 bytes and contains the source port.
	udpSourcePort = udpHeaderUnpacked[0]
	
	# The second H is 2 bytes and contains the destination port.
	udpDestPort = udpHeaderUnpacked[1]
	
	# The third H is 2 bytes and contains the packet length.
	udpLength = udpHeaderUnpacked[2]
	
	# The fourth H is 2 bytes and contains the header checksum.
	udpChecksum = udpHeaderUnpacked[3]
	
	# Print UDP Header
	print('\n*******************\n******* UDP *******\n*******************' +
	'\nSource Port: ' + str(udpSourcePort) +
	'\nDestination Port: ' + str(udpDestPort) +
	'\nLength: ' + str(udpLength) + ' bytes' +
	'\nChecksum: ' + format(udpChecksum, '#04X'))

def start():
	# Ask the user if they would like to begin the sniffer or not.
	decision = raw_input('Hello, would you like to sniff the network? Y/N: ')

	# Y runs the rest of the application.
	# N exits the application.
	if (decision == 'Y') or (decision == 'y'):
		print('Sniffing, press Ctrl+c to cancel...')
	elif (decision == 'N') or (decision == 'n'):
		close()

def close():
	# Exit the application.
	print('Goodbye.')
	time.sleep(1)
	sys.exit()

def sniff():
	# Ask the user to begin.
	start()
	
	# Know what platform the application is running on.
	plat = platform.system()
	
	try:
		# If Linux, set up the raw socket the Linux way.
		# If Windows, set up the raw socket the Windows way.
		# If not Linux or Windows, close the application.
		if plat == 'Linux':
			# Create the raw socket.
			sock = socket.socket(socket.AF_PACKET , socket.SOCK_RAW , socket.ntohs(0x0003))
			
			# Sniff packets. Will loop until user presses Ctrl+c.
			while True:	
				# Recieve the packets in the network.
				# Packet will be a tuple, use the first element in the tuple.
				packet = sock.recvfrom(65565)
				packet = packet[0]
				
				# Unpack the Ethernet (MAC) information.
				begin = 0
				end = constEthHeaderLength
				ethType = eth(packet, begin, end)
				
				# Find if the Ethernet frame is ARP or IP.
				begin = constEthHeaderLength
				if ethType == 1544:
					# Unpack the ARP information.
					end = begin + constARPLength
					arp(packet, begin, end)
				elif ethType == 8:
					# Unpack the IP information.
					end = begin + constIPHeaderLength
					ipProtocol = ip(packet, begin, end)
					
					# If the protocol is 1, meaning ICMP, then unpack the ICMP information.
					# If the protocol is 6, meaning TCP, then unpack the TCP information.
					# If the protocol is 17, meaning UDP, then unpack the UDP information.
					begin = constEthHeaderLength + constIPHeaderLength
					if ipProtocol == 1:
						end = begin + constICMPHeaderLength
						icmp(packet, begin, end)
					elif ipProtocol == 6:
						end = begin + constTCPHeaderLength
						tcp(packet, begin, end)
					elif ipProtocol == 17:
						end = begin + constUDPHeaderLength
						udp(packet, begin, end)
						
					print('\n----------------------------------------')
					
			# Close the socket.
			sock.close()
		elif plat == 'Windows':
			# The public network interface.
			HOST = socket.gethostbyname(socket.gethostname())

			# Create a raw socket and bind it to the public interface.
			sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
			sock.bind((HOST, 0))

			# Include IP headers
			sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

			# Receive all packages.
			sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
			
			# Sniff packets. Will loop until user presses Ctrl+c.
			while True:	
				# Recieve the packets in the network.
				# Packet will be a tuple, use the first element in the tuple.
				packet = sock.recvfrom(65565)
				packet = packet[0]
				
				# Unpack the IP information.
				begin = 0
				end = constIPHeaderLength
				ipProtocol = ip(packet, begin, end)
				
				# If the protocol is 1, meaning ICMP, then unpack the ICMP information.
				# If the protocol is 6, meaning TCP, then unpack the TCP information.
				# If the protocol is 17, meaning UDP, then unpack the UDP information.
				begin = constIPHeaderLength
				if ipProtocol == 1:
					end = begin + constICMPHeaderLength
					icmp(packet, begin, end)
				elif ipProtocol == 6:
					end = begin + constTCPHeaderLength
					tcp(packet, begin, end)
				elif ipProtocol == 17:
					end = begin + constUDPHeaderLength
					udp(packet, begin, end)
					
				print('\n----------------------------------------')	
			
			# Disable promiscuous mode.	
			sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
			
			# Close the socket.
			sock.close()
		else:
			print('The OS you are running is not supported.')
			
	except socket.error, msg:
		print('Socket could not be created. \nError code: ' + str(msg[0]) + '\nMessage: ' + msg[1])
	except KeyboardInterrupt:
		print "\nSniffing stopped."   
	
	close()  

def main():
	sniff()

if __name__ == "__main__":
	main()
