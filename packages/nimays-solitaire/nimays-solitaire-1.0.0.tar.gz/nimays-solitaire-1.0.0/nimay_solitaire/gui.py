import copy
import os
import pygame

from nimay_solitaire.card import Card
from nimay_solitaire.solitaire import Solitaire
from time import sleep


class GUI(object):
    """
    A class responsible for rendering a graphical user interface and invoking responses to user interaction with the GUI
    """

    green = (0, 150, 0)
    blue = (0, 0, 150)
    red = (150, 0, 0)
    black = (0, 0, 0)
    white = (255, 255, 255)
    background_colors = [green, blue, red, black]
    img_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'images')

    """
    Initialize the GUI
    """
    def __init__(self):
        self.solitaire = Solitaire(loop=False)
        pygame.init()
        self.display_width = 1000
        self.display_height = 600
        self.background_color_idx = 0
        self.card_w = 69
        self.card_h = 100
        self.game_display = pygame.display.set_mode((self.display_width, self.display_height))
        pygame.display.set_caption("Nimay's Solitaire")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(pygame.font.get_default_font(), 12)

        self.new_game_button, self.undo_button, self.end_game_button, self.change_background_button = None, None, None, None
        self.display_buttons()

        self.new_game_button = pygame.draw.rect(self.game_display, self.white, (150, 450, 100, 50))
        self.small_text = pygame.font.Font(pygame.font.get_default_font(), 20)

        self.stock_pile, self.waste_pile = None, None
        self.tableau_piles = None
        self.foundation_piles = [None for _ in range(self.solitaire.gameboard.num_foundation_piles)]
        self.game_loop()

    """
    Display the new game, undo move, and end game buttons on the game display
    """
    def display_buttons(self):
        button_x = 25
        button_w = self.card_w
        button_h = 25
        button_pad = 25
        # End game button
        self.end_game_button = pygame.draw.rect(self.game_display, self.white,
                         (button_x, self.display_height - button_pad - button_h, button_w, button_h))
        text_surface, text_rect = self.text_objects("END GAME", self.font)
        text_rect.center = self.end_game_button.center
        self.game_display.blit(text_surface, text_rect)
        # Undo move button
        self.undo_button = pygame.draw.rect(self.game_display, self.white,
                         (button_x, self.display_height - 2*(button_pad + button_h), button_w, button_h))
        text_surface, text_rect = self.text_objects("UNDO", self.font)
        text_rect.center = self.undo_button.center
        self.game_display.blit(text_surface, text_rect)
        # Restart game button
        self.new_game_button = pygame.draw.rect(self.game_display, self.white,
                                                (button_x, self.display_height - 3*(button_pad + button_h), button_w, button_h))
        text_surface, text_rect = self.text_objects("NEW GAME", self.font)
        text_rect.center = self.new_game_button.center
        self.game_display.blit(text_surface, text_rect)
        # Change background button
        self.change_background_button = pygame.draw.rect(self.game_display, self.white,
                                            (button_x, self.display_height - 4*(button_pad + button_h), button_w + 35, button_h))
        text_surface, text_rect = self.text_objects("CHANGE COLOR", self.font)
        text_rect.center = self.change_background_button.center
        self.game_display.blit(text_surface, text_rect)

    """
    Display the gameboard on the game display
    """
    def display_gameboard(self):
        self.display_deck()
        self.display_tableau_piles()
        self.display_foundation_piles()

    """
    Display the tableau piles on the game display
    """
    def display_tableau_piles(self):
        tableau_piles = self.solitaire.gameboard.tableau_piles
        tableau_rects = []
        for i in range(len(tableau_piles)):
            card_rects = []
            # Cards should overlap, leaving the top 25 pixels of covered cards visible
            x_offset = 25 + self.card_w
            x = 50 + x_offset * (i+1)
            y = 25
            if not tableau_piles[i].cards:
                card_rects.append(pygame.draw.rect(self.game_display, self.background_colors[self.background_color_idx],
                                                   (x, y, self.card_w, self.card_h)))
            else:
                for j in range(len(tableau_piles[i].cards)):
                    card_rects.append(pygame.draw.rect(self.game_display, self.white, (x, (j+1)*y, self.card_w, self.card_h)))
                    self.display_card(tableau_piles[i].cards[j], (x, (j+1)*y))
            tableau_rects.append(card_rects)
        self.tableau_piles = tableau_rects

    """
    Display the foundation piles on the game display
    """
    def display_foundation_piles(self):
        segment_height = self.display_height / 4
        segment_x = self.display_width - 25 - self.card_w
        foundation_piles = self.solitaire.gameboard.foundation_piles
        for i in range(4):
            segment_start = i*segment_height
            segment_pad = (segment_height - self.card_h) / 2
            segment_y = segment_start + segment_pad
            dimensions = (segment_x, segment_y, self.card_w, self.card_h)
            self.foundation_piles[i] = pygame.draw.rect(self.game_display, self.white, dimensions)
            if foundation_piles[i].cards:
                self.display_card(foundation_piles[i].cards[-1], (segment_x, segment_y))
            # Place holder text to know which pile belongs to which suit
            else:
                text_surface, text_rect = self.text_objects(Card.suits[i] + 's', self.font)
                text_rect.center = self.foundation_piles[i].center
                self.game_display.blit(text_surface, text_rect)

    """
    Display the deck on the game display
    """
    def display_deck(self):
        stock_pile = self.solitaire.gameboard.deck.stock_pile
        waste_pile = self.solitaire.gameboard.deck.waste_pile
        # stock pile rect
        if stock_pile.cards:
            stock_x, stock_y = 25, 25
            self.stock_pile = pygame.draw.rect(self.game_display, self.white, (stock_x, stock_y, self.card_w, self.card_h))
            self.display_card(stock_pile.cards[-1], (stock_x, stock_y))
        # waste pile rect
        if waste_pile.cards:
            waste_x, waste_y = 25, 25 * 2 + self.card_h
            self.waste_pile = pygame.draw.rect(self.game_display, self.white, (waste_x, waste_y, self.card_w, self.card_h))
            self.display_card(waste_pile.cards[-1], (waste_x, waste_y))

    """
    Get the front image of a card
    :param card: The card to get the front image for.
    """
    def _get_card_front_image(self, card):
        filename = str(card).replace(' ', '_') + '.png'
        img = pygame.image.load(os.path.join(self.img_path, filename))
        return pygame.transform.scale(img, (self.card_w, self.card_h))

    """
    Get the back image of a card
    """
    def _get_card_back_image(self):
        filename = 'back.png'
        img = pygame.image.load(os.path.join(self.img_path, filename))
        return pygame.transform.scale(img, (self.card_w, self.card_h))

    """
    Displays a card on the game display.
    :param card: The card to display
    :param location: The x y coordinates to display the card at
    """
    def display_card(self, card, location):
        if card.visible:
            self.game_display.blit(self._get_card_front_image(card), location)
        else:
            self.game_display.blit(self._get_card_back_image(), location)

    """
    Generate objects to render text.
    :param text: A string of text to generate objects for
    :param font: The font to generate objects in
    :return: A surface and its corresponding rectangle
    """
    def text_objects(self, text, font):
        text_surface = font.render(text, True, self.black)
        return text_surface, text_surface.get_rect()

    """
    Returns the position of the clicked foundation pile.
    :param mouse_pos: An integer tuple of the form (x, y) that represents the location that the mouse was clicked at
    :return: The index of the foundation pile that was clicked if one was clicked, None otherwise.
    """
    def get_selected_foundation_idx(self, mouse_pos):
        for i, pile_rect in enumerate(self.foundation_piles):
            if pile_rect and pile_rect.collidepoint(mouse_pos):
                return i
        return None

    """
    Determines whether the user clicked on the waste pile.
    :param mouse_pos: An integer tuple of the form (x, y) that represents the location that the mouse was clicked at
    :return: True if the waste pile was selected, False otherwise
    """
    def waste_pile_selected(self, mouse_pos):
        return self.waste_pile and self.waste_pile.collidepoint(mouse_pos)

    """
    Determines whether the user clicked on a tableau pile.
    :param mouse_pos: An integer tuple of the form (x, y) that represents the location that the mouse was clicked at
    :return: True if a tableau pile was selected, False otherwise
    """
    def tableau_pile_selected(self, mouse_pos):
        if self.tableau_piles:
            for pile in self.tableau_piles:
                for card_rect in pile:
                    if card_rect.collidepoint(mouse_pos):
                        return True
        return False

    """
    Determines the tableau pile index and the card index within the tableau pile that the user selected. Assumes that
    tableau_pile_selected() has been called and returned True for the same mouse_pos that is passed into this function.
    :param mouse_pos: An integer tuple of the form (x, y) that represents the location that the mouse was clicked at
    :return: tableau pile index, card index
    """
    def get_selected_tableau_pile(self, mouse_pos):
        for i, pile in enumerate(self.tableau_piles):
            for j, card_rect in enumerate(pile):
                if card_rect.collidepoint(mouse_pos):
                    return i, self.get_selected_card_in_tableau_pile(i, mouse_pos)
        # This should never happen, make sure to use the tableau_pile_selected() safety check
        return None, None

    """
    Get the index of the card that was selected within the given tableau pile.
    :param tab_idx: The index of the tableau pile to check in
    :param mouse_pos: An integer tuple of the form (x, y) that represents the location that the mouse was clicked at
    :return: index of selected card within the provided tableau pile
    """
    def get_selected_card_in_tableau_pile(self, tab_idx, mouse_pos):
        pile = self.tableau_piles[tab_idx]
        for i in range(len(pile) - 1):
            card_rect = pile[i]
            next_card_rect = pile[i + 1]
            if card_rect.collidepoint(mouse_pos) and not next_card_rect.collidepoint(mouse_pos):
                return i
        return len(pile) - 1

    """
    Display special effects when the player wins the game.
    """
    def game_end_effects(self):
        for i in range(4):
            self.foundation_piles.append(self._get_card_front_image(Card(Card.HEART, 0, True)))
        filename = 'win.jpg'
        background = pygame.Surface((self.display_width, self.display_height))
        background.fill(self.white)
        img = pygame.image.load(os.path.join(self.img_path, filename))
        img = pygame.transform.scale(img, (self.display_width, self.display_height))
        img = img.convert()
        rect = img.get_rect()
        stop = False
        while not stop:
            img.set_alpha(i)
            self.game_display.fill((255, 255, 255))
            self.game_display.blit(background, background.get_rect())
            self.game_display.blit(img, rect)
            pygame.time.delay(20)
            i += 1
            if i == 255:
                stop = True
            pygame.display.update()

    def game_loop(self):
        move_str = None
        move_str_complete = False
        update_display = True
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if self.new_game_button.collidepoint(mouse_pos):
                        self.solitaire = Solitaire(loop=False)
                    elif self.undo_button.collidepoint(mouse_pos):
                        self.solitaire.undo_move()
                    elif self.end_game_button.collidepoint(mouse_pos):
                        pygame.quit()
                        quit()
                    elif self.change_background_button.collidepoint(mouse_pos):
                        self.background_color_idx = (1 + self.background_color_idx) % len(self.background_colors)
                    elif self.stock_pile.collidepoint(mouse_pos):
                        self.solitaire.make_move_with_history("MOVE D")
                    elif self.get_selected_foundation_idx(mouse_pos) is not None:
                        if move_str:
                            # Moving the foundation pile does not take the card index argument
                            if move_str[5] == 'T':
                                move_str = ' '.join(move_str.split()[:3])
                            move_str += " F"
                            move_str_complete = True
                        else:
                            move_str = "MOVE F " + str(self.get_selected_foundation_idx(mouse_pos))
                    elif self.waste_pile_selected(mouse_pos):
                        move_str = "MOVE W"
                    elif self.tableau_pile_selected(mouse_pos):
                        pile_idx, card_idx = self.get_selected_tableau_pile(mouse_pos)
                        if move_str:
                            move_str += " T " + str(pile_idx)
                            move_str_complete = True
                        else:
                            move_str = "MOVE T " + str(pile_idx) + " " + str(card_idx)
                    if move_str_complete:
                        self.solitaire.make_move_with_history(move_str)
                        move_str = None
                        move_str_complete = False
                update_display = True

            if self.solitaire.game_end():
                self.game_end_effects()
                break

            if update_display:
                self.game_display.fill(self.background_colors[self.background_color_idx])
                self.display_gameboard()
                self.display_buttons()
                update_display = False

            pygame.display.update()
            self.clock.tick(15)
