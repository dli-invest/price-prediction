def color_returns(val):
    """
    Takes a scalar and returns red for significantly negative returns,
    green for signficantly positive returns and black otherwise.
    """ 
    if isinstance(val, str):
      return ''
    if val < -0.1:
      color = 'red'
    elif val > 0.1:
      color = 'green'
    else: 
      color = 'black'
    return 'color: %s' % color


def apply_returns_styling(df, className='class="table-alternating"', caption="Returns"):
    """
      Description: generates a styled returns html table 

      Parameters:
          df: Pandas Dataframe
          className: class attribute of html table
          caption: Table caption
      Returns:
          styled html table
    """
    valid_df = df.reset_index()
    return valid_df.style\
      .set_table_attributes(className)\
      .set_caption(caption)\
      .applymap(color_returns)\
      .render()
