import scripts


def main():
    scripts.find_players('BR1', 'Luckmann', 1613358000000, 1613962800000, 10)
    scripts.find_matches('BR1')
    scripts.gather_players_match_history_daily('BR1', 'accountID', 1613358000000, 1613962800000)


if __name__ == '__main__':
    main()
