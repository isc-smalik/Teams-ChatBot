
    async def __send_thumbnail_card(self, turn_context:TurnContext):
        card = ThumbnailCard()
        card.images = [CardImage(url="https://raw.githubusercontent.com/intersystems-community/sqltools-intersystems-driver/master/icons/default.png")]
        card.title = (f'{trak_name}')
        card.subtitle = (f"Record Number : {trak_recordNumber}")
        card.subtitle = (f"DOB : {trak_dob}")
        card.subtitle = (f"Sex : {trak_gender}")
        card.subtitle = (f"Care Provider : {trak_careProvider}")
        card.text = "Notes come here"
            
        return await turn_context.send_activity(
            MessageFactory.attachment(CardFactory.thumbnail_card(card))
        )

    async def __send_receipt_card(self, turn_context:TurnContext):
        card = ReceiptCard()
        card.title = (f'{trak_name}')
        card.facts = [
            Fact(key="Record Number",value= trak_recordNumber),
            Fact(key="DOB",value= trak_dob),
            Fact(key="Sex",value=trak_gender),
            Fact(key="Care Provider", value=trak_careProvider)
        ]
        '''
        card.items = [
            ReceiptItem(title="Bot Framework book",price="20Euro"),
            ReceiptItem(title="Python Book",price="100 Euro")
        ]'''
        #card.vat = "0.2"
        #card.tax = "12%"
        #card.total = "180"

        return await turn_context.send_activity(
            MessageFactory.attachment(CardFactory.receipt_card(card))
        )

    async def __send_intro_card(self, turn_context: TurnContext):
        card = HeroCard(
            title=(f"Portal to TrakCare"),
            text= (f"Click the button below to go to {trak_name} TrakCare profile"),
            images=[CardImage(url="https://www.hhmglobal.com/wp-content/uploads/news/26893/InterSystems_TrakCare.png")],
            buttons=[
                CardAction(
                    type=ActionTypes.open_url,
                    title="Go to trakacare",
                    text="Go to trakacare",
                    display_text="Go to trakacare",
                    value= (trak_url),
                ),
            ],
        )

        return await turn_context.send_activity(
            MessageFactory.attachment(CardFactory.hero_card(card))
        )"""