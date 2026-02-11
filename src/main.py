from analyzer import find_thunderbird_profile
from gui import show_gui


def main():
    """Main entry point for the application."""
    tb_profile = find_thunderbird_profile()
    
    if tb_profile:
        show_gui(tb_profile)
    else:
        print("Could not find Thunderbird profile. Exiting.")


if __name__ == "__main__":
    main()
