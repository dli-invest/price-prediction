import pandas as pd
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


def apply_returns_styling(
      df,
      className='class="table-alternating"',
      caption="Returns",
      columns=[]
    ):
    """
      Description: generates a styled returns html table 

      Parameters:
          df: Pandas Dataframe
          className: class attribute of html table
          caption: Table caption
          columns: columns that styling is applied to
      Returns:
          styled html table
    """
    valid_df = df.reset_index(drop=False)
    return valid_df.style.\
      set_table_attributes(className).\
      set_caption(caption).\
      applymap(color_returns, subset=pd.IndexSlice[:, columns]).\
      render()
