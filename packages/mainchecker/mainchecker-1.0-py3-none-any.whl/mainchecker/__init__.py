def check_for_main(name = __name__):
    if __name__ == name:
        raise Exception('Do not launch this program directly, but import it.')
		
if __name__ == '__main__':
	check_for_main()