require('dotenv').config();

const { Client } = require('@notionhq/client');

const notion = new Client({ auth: process.env.NOTION_API_KEY });

(async () => {
  const response = await notion.search({
    query: 'scottcarr',
    filter: {
      value: 'page',
      property: 'object'
    },
    sort: {
      direction: 'ascending',
      timestamp: 'last_edited_time'
    },
  });
  // Extracting the IDs from the response
  console.log(response);
  const pageIds = response.results.map(page => page.id);
  
  // Logging out the IDs
  console.log(pageIds);

})();